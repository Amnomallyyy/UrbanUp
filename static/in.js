var output = document.getElementById("chatAI");
var messageInput = document.getElementById("vl");
var ChatWithAI = document.getElementById("chatwithai");
var display = document.getElementById("Output")
var auditAI = document.getElementById("auditAI");
var Save = document.getElementById("Save" )
var Clear = document.getElementById("clearEntryFileDatabase")

function createButtonElement(filename) {
  
    const container = document.createElement('div');
    
   
    container.className = "button-container"; 

    const myButton = document.createElement('button');

    myButton.textContent = '$filename';

    // 4. Attach the event listener you already know how to write!
    myButton.addEventListener('click', function() {
        window.location.href = "https://www.example.com"; // Your redirect logic here
    });

    // 5. Put the button INSIDE the container
    container.appendChild(myButton);

    // 6. Finally, attach the container to your actual webpage (e.g., the body)
    document.body.appendChild(container);
}

// Call the function to make the button appear
createButtonElement();

async function sendMessage(){

    var text = messageInput.value;
    

    if(text == ""){
        return;
    }
     addMessage(text, "user");

     messageInput.value = "";


    const response = await fetch("/chat"
    ,{
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({message: text})
    }).then(function(response){


        console.log(response);
        return response.json();


    }).then(function(data){


        console.log(data);
        addMessage(data.reply, "bot")

    })
   
 

    
    }
    


    async function audit(){

        const response = fetch("/auditAI",
            {method : "POST"}).then(function(response){
                console.log(response)
                console.log("this button was clicked")
        })}
  
function savefunc(){
 
    console.log("The save Button Was pushed")


}
function clearfunc(){
 
    console.log("The clear Button Was pushed")


}
ChatWithAI.addEventListener("click",sendMessage)
auditAI.addEventListener("click", audit)
Save.addEventListener("click", savefunc)
Clear.addEventListener("click",clearfunc)