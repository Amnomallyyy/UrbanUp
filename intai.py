import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
import numpy as np
from google import genai
from pydantic import BaseModel, Field
from google.genai.errors import APIError






class AuditReport(BaseModel):
    sustainability_score: int = Field(description="Score from 0-100 based strictly on SDG math.")
    critical_warnings: list[str] = Field(description="Specific SDG or zoning violations found.")
    positive_highlights: list[str] = Field(description="Adherence to SDG goals.")
    actionable_advice: list[str] = Field(description="Strict, directional advice to improve the layout.")
import math

ZONE_TYPES = {
    "apartments": "residential",
    "suburban home": "residential",
    "villas": "residential",
    "farmhouse": "residential",
    "shops": "commercial",
    "malls": "commercial",
    "skyscraper": "commercial",
    "factory": "industrial",
    "power_plant": "utility",
    "park": "park",
    "tree_oak": "park",
    "utility": "utility"
}

AREA_ESTIMATES_SQM = {
    "apartments": 2500,
    "suburban home": 400,
    "villas": 1200,
    "farmhouse": 5000,
    "shops": 300,
    "malls": 15000,
    "skyscraper": 4000,
    "factory": 20000,
    "power_plant": 10000,
    "park": 8000,
    "tree_oak": 20,

}


def haversine_distance_m(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def compute_metrics(nodes):
    categorized = {
        "residential": [],
        "industrial": [],
        "commercial": [],
        "park": [],
        "utility": []
    }

    total_concrete_area = 0.0
    total_green_area = 0.0

   

    for node in nodes:
        frontend_name = node.get("name", "").lower()
        lat = node.get("lat")
        lng = node.get("lng")

        if lat is None or lng is None:
            continue

        backend_category = ZONE_TYPES.get(frontend_name, "unknown")

        mapped_item = {"lat": lat, "lng": lng, "type": frontend_name}

        if backend_category in categorized:
            categorized[backend_category].append(mapped_item)

        item_area = AREA_ESTIMATES_SQM.get(frontend_name, 500)

        if backend_category == "park":
            total_green_area += item_area
        else:
            total_concrete_area += item_area

    residential = categorized["residential"]
    industrial = categorized["industrial"]
    commercial = categorized["commercial"]
    parks = categorized["park"]
    utilities = categorized["utility"]

    metrics = {}
    PENALTY_DISTANCE = 99999.0

    # Metric 1: Public Health
    if len(residential) > 0 and len(industrial) > 0:
        min_dist = PENALTY_DISTANCE
        for r in residential:
            for i in industrial:
                dist = haversine_distance_m(r["lat"], r["lng"], i["lat"], i["lng"])
                if dist < min_dist:
                    min_dist = dist
        metrics["min_industrial_residential_distance_m"] = round(min_dist, 1)
    else:
        metrics["min_industrial_residential_distance_m"] = "No industrial zones present (Safe)"

    # Metric 2: 15-Minute City
    def avg_nearest_distance(source_list, target_list):
        if len(source_list) == 0:
            return 0.0
        if len(target_list) == 0:
            return PENALTY_DISTANCE
        total_distance = 0.0
        for s in source_list:
            nearest_target_dist = PENALTY_DISTANCE
            for t in target_list:
                dist = haversine_distance_m(s["lat"], s["lng"], t["lat"], t["lng"])
                if dist < nearest_target_dist:
                    nearest_target_dist = dist
            total_distance += nearest_target_dist
        return round(total_distance / len(source_list), 1)

    metrics["residential_commercial_avg_distance_m"] = avg_nearest_distance(residential, commercial)
    metrics["residential_park_avg_distance_m"] = avg_nearest_distance(residential, parks)

    # Metric 3: Utilities Coverage
    def count_stranded(zone_list):
        stranded_count = 0
        if len(zone_list) > 0:
            if len(utilities) == 0:
                return len(zone_list)
            for z in zone_list:
                has_utility = False
                for u in utilities:
                    dist = haversine_distance_m(z["lat"], z["lng"], u["lat"], u["lng"])
                    if dist <= 1000.0:
                        has_utility = True
                        break
                if not has_utility:
                    stranded_count += 1
        return stranded_count

    metrics["homes_without_utilities"] = count_stranded(residential)
    metrics["commercial_without_utilities"] = count_stranded(commercial)
    metrics["industrial_without_utilities"] = count_stranded(industrial)

    # Metric 4: Environmental Balance
    total_city_area = total_green_area + total_concrete_area
    if total_city_area > 0:
        ratio = (total_green_area / total_city_area) * 100
        metrics["green_space_percentage"] = round(ratio, 1)
    else:
        metrics["green_space_percentage"] = 0.0

    return metrics


def run_audit(objectives, map_state):
    print("--- RUN_AUDIT STARTED ---")
    
    try:
        # STEP 1: The Math Engine
        print("Step 1: Running compute_metrics...")
        metrics = compute_metrics(map_state)
        print("Step 1 Complete! Math calculated.")

        # STEP 2: The Prompt formulation
        print("Step 2: Building AI prompt...")
        factual_prompt = f"""
        You are an Urban Planning Auditor. Evaluate the layout strictly based on the math provided.

        USER OBJECTIVE: "{objectives}"

        DETERMINISTIC CITY MATH (Ground Truth):
        - Green Space Percentage: {metrics.get('green_space_percentage', 0)}% (Goal is >15%)
        - Closest Factory to Housing: {metrics.get('min_industrial_residential_distance_m', 0)} meters (Goal >500m)
        - Average Commute to Shops: {metrics.get('residential_commercial_avg_distance_m', 0)} meters (Goal <800m)
        - Average Walk to Parks: {metrics.get('residential_park_avg_distance_m', 0)} meters (Goal <800m)
        - Homes Without Utility Access: {metrics.get('homes_without_utilities', 0)} (Must be 0)
        - Commercial Zones Without Utility Access: {metrics.get('commercial_without_utilities', 0)} (Must be 0)
        - Industrial Zones Without Utility Access: {metrics.get('industrial_without_utilities', 0)} (Must be 0)
        """
        print("Step 2 Complete!")

        # STEP 3: The API Call
        print("Step 3: Calling Gemini API...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=factual_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AuditReport, 
                system_instruction="Evaluate the metrics against the rules. Output ONLY JSON.",
                temperature=0.0
            )
        )
        print("Step 3 Complete! AI responded.")

        # STEP 4: Validation
        if not response or not response.text:
            print("Step 4 FAILED: AI returned None or empty text.")
            return '{"error": "The AI returned an empty response. It might be blocking the request."}'
            
        print("--- RUN_AUDIT SUCCESS ---")
        return response.text

    except Exception as e:
        # IF ANYTHING CRASHES, IT CATCHES HERE AND RETURNS A SAFE JSON STRING
        print(f"!!! CRASH INSIDE RUN_AUDIT !!! -> {e}")
        safe_error_msg = str(e).replace('"', "'") 
        return f'{{"error": "Internal AI/Math Failure: {safe_error_msg}"}}'



def validate_structures(map_state, user_memo):

    if not isinstance(map_state, dict):
        return '{"error": "System fault: Expected map_state to be a dictionary."}'

    if not isinstance(user_memo, str):
        return '{"error": "System fault: Expected user_memo to be a string."}'

    if len(map_state) == 0:
        return '{"error": "Action Rejected: The map canvas is completely empty. Please place infrastructure to run an audit."}'

    if len(user_memo.strip()) == 0:
        return '{"error": "Action Rejected: No urban planning objective provided. Please define your goals."}'

    return None







# --- CHATBOT (Interactions API) ---

CHAT_SYSTEM_INSTRUCTION = """
You are a friendly, professional Urban Planning Consultant. You may engage in brief, polite small talk if the user initiates it, but you must always seamlessly pivot the conversation back to their city metrics, 
the UN Sustainable Development Goals, or their stated Memo.
Your goal is to help the user design a sustainable city.
You will occasionally receive [SYSTEM UPDATE] messages containing audit scores. 
DO NOT output raw JSON. Speak conversationally, professionally, and directly to the user.
Always end your response with a thoughtful follow-up question that moves the design forward.
"""

def chat_bot(user_message, interaction_id=None):
    kwargs = {
        "model": "gemini-2.5-flash",
        "input": user_message,
    }

    if interaction_id is None:
        kwargs["system_instruction"] = CHAT_SYSTEM_INSTRUCTION
    else:
        kwargs["previous_interaction_id"] = interaction_id

    response = client.interactions.create(**kwargs)

    return {
        "text_reply": response.output_text,
        "new_interaction_id": response.id 
    }


def parse_audit_for_chatbot(audit_json_string):

    import json
    data = json.loads(audit_json_string)

    hidden_prompt = f"""
[SYSTEM UPDATE: INVISIBLE TO USER]
An audit was just run on the map. The new sustainability score is: {data['sustainability_score']}.
Warnings found: {', '.join(data['critical_warnings'])}.
Acknowledge the user's latest action and provide human-like advice based on these numbers,
then ask a good follow-up question to keep the design conversation moving.
""".strip()

    return hidden_prompt












  
    