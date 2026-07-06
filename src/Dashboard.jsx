import React, { useState } from 'react';
import pixelatedShopImg from './assets/pixelatedshop.jpg';
import pixelatedAppImg from './assets/pixelatedappartments.jpg';

export default function Dashboard() {
   const assets = [
    { id: 'Commercial', name: 'Shops', icon: pixelatedShopImg },
    { id: 'Residential', name:'Appartments', icon: pixelatedAppImg }
  ];
  const [activeAssetId, setActiveAssetId] = useState(null);
  const [placedItems, setPlacedItems] = useState([]);
  const handleViewportClick = (e) => {
    if (!activeAssetId) return;

    const elementSize = 40;
    const rect = e.currentTarget.getBoundingClientRect();
    const xPosition = e.clientX - rect.left - elementSize / 2;
    const yPosition = e.clientY - rect.top - elementSize / 2;

    const currentAsset = assets.find(a => a.id === activeAssetId);

    const newItem = {
      uniqueId: Date.now(),
      imgUrl: currentAsset.icon,
      alt: currentAsset.name,
      x: xPosition,
      y: yPosition
    };

    setPlacedItems([...placedItems, newItem]);
  };
  
  return (
    
        
    <div className="bg-sky-100 text-slate-100 min-h-screen font-sans antialiased flex flex-col">
      {}
    <header className="h-16 border-b border-sky-400 flex items-center justify-between px-6 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div>
          <h1 class="text-xl font-bold tracking-tight text-white">Urban Development Workspace</h1>
          <p class="text-xs text-slate-400">Responsive Grid Blueprint</p>
        </div>
      </header>

      
        <div className="p-4 grid grid-cols-1 lg:grid-cols-12 gap-4 h-[calc(100vh-64px)] w-full flex-1 items-stretch">
        {''}
         <aside className="lg:col-span-3 bg-sky-400 border border-slate-700 rounded-xl p-4 flex flex-col justify-between overflow-y-auto">
     
          <div>
            <h2 className="text-lg font-bold mb-2 text-white">Asset Catalog</h2>
            <p className="text-xs text-slate-400 mb-4">Select or drag components to the map viewport</p>
            <div id="asset-drawer-root" className="space-y-4">

            {'Commercial'}
            <div>
            
           <button 
            onClick={() => setActiveAssetId(activeAssetId === 'Commercial' ? null : 'Commercial')}
            className={`p-3 border text-left rounded-lg text-xs transition-colors w-full ${
            activeAssetId === 'Commercial' ? 'border-sky-500 bg-sky-500/10' : 'bg-slate-900 border-slate-700 hover:border-slate-500'
            }`}
            >
            <span className="font-medium text-white block pointer-events-none">Shops</span>
            <span className="text-[10px] text-slate-500 pointer-events-none">Density: High</span>
            </button>
            <div className="p-3 bg-slate-900 border border-slate-700 rounded-lg text-xs hover:border-sky-500 cursor-grab transition-colors">
            <span className="font-medium text-white block">Department Stores</span>
            <span className="text-[10px] text-slate-500">Density: Low</span>
            </div>
            <div className="p-3 bg-slate-900 border border-slate-700 rounded-lg text-xs hover:border-sky-500 cursor-grab transition-colors">
            <span className="font-medium text-white block">Skyscraper</span>
            <span className="text-[10px] text-slate-500">Density: Very Low</span>
            </div>
          </div>
        


            {'Residential'}
            <div>
            <button 
            onClick={() => setActiveAssetId(activeAssetId === 'Residential' ? null : 'Residential')}
            className={`p-3 border text-left rounded-lg text-xs transition-colors w-full ${
            activeAssetId === 'Residential' ? 'border-sky-500 bg-sky-500/10' : 'bg-slate-900 border-slate-700 hover:border-slate-500'
            }`}
            >
            <span className="font-medium text-white block pointer-events-none">High-Rise Appartment</span>
            <span className="text-[10px] text-slate-500 pointer-events-none">Density: High</span>
            </button>
            <div className="p-3 bg-slate-900 border border-slate-700 rounded-lg text-xs hover:border-sky-500 cursor-grab transition-colors">
            <span className="font-medium text-white block">Suburban Home</span>
            <span className="text-[10px] text-slate-500">Density: Low</span>
            </div>
            <div className="p-3 bg-slate-900 border border-slate-700 rounded-lg text-xs hover:border-sky-500 cursor-grab transition-colors">
            <span className="font-medium text-white block"> Villas</span>
            <span className="text-[10px] text-slate-500">Density: Very Low</span>
            </div>
            <div className="p-3 bg-slate-900 border border-slate-700 rounded-lg text-xs hover:border-sky-500 cursor-grab transition-colors">
            <span className="font-medium text-white block"> Farmhouse </span>
            <span className="text-[10px] text-slate-500">Density: Very Low</span>
            </div>
            </div>
        
            </div>
          </div>
          
        </aside>

        {''}
    <main 
        onClick={handleViewportClick}
        className="lg:col-span-6 bg-slate-950 border-2 border-double border-slate-700 rounded-xl relative flex flex-col items-center justify-center overflow-hidden group hover:border-sky-500 transition-colors cursor-crosshair">
        <div className="absolute inset-0 bg-[radial-gradient(#bae6fd_1px,transparent_1px)] [background-size:16px_16px] opacity-40 pointer-events-none"></div>
        
        <div className="text-center z-10 pointer-events-none">
        <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-100/10 text-sky-400 border border-sky-500/20">
        Interactive viewport
        </span>
         <p className="text-sm text-slate-400 mt-2">Select "Shops" on the left, then click inside this grid to build.</p>
        </div>
        {placedItems.map((item) => (
        <img
        key={item.uniqueId}
        src={item.imgUrl}
        alt={item.alt}
        className="absolute pointer-events-none"
        style={{
        width: '40px',
        height: '40px',
        left: `${item.x}px`,
        top: `${item.y}px`,
    }}
    />
    ))}
    </main>

        {''}
        <aside className="lg:col-span-3 bg-slate-800 border border-slate-700 rounded-xl p-4 flex flex-col h-full overflow-y-auto">
          <h2 className="text-lg font-semibold mb-2 text-white">AI Audit Hub</h2>
          <p className="text-xs text-slate-400 mb-4">Real-time compliance</p>

          <div className="space-y-3 flex-1">
            <div className="p-3 bg-slate-900/50 border border-slate-700 rounded-lg text-xs">
              <span className="text-slate-400 font-semibold block mb-1">System Evaluation Pending</span>
              Awaiting asset placement to initialize structural layout audit.
            </div>
          </div>
        </aside>

      </div>
    </div>
  );
}


