import { useState } from "react";
import Layout from "@/react-app/components/Layout";
import ProductCard from "@/react-app/components/ProductCard";
import { useStore } from "@/shared/store";

const tabs = ["outfits", "productos", "armario", "pedidos"] as const;

type Tab = typeof tabs[number];

export default function Profile() {
  const { user, looks, products, wardrobe, orders } = useStore();
  const [tab, setTab] = useState<Tab>("outfits");
  const wardrobeProducts = products.filter((p) => wardrobe.includes(p.id));

  return (
    <Layout>
      <div className="p-4">
        <div className="flex items-center gap-4 mb-4">
          <img src={user.avatar} alt={user.name} className="w-20 h-20 rounded-full" />
          <div>
            <p className="font-semibold">{user.name}</p>
            <p className="text-gray-500">@{user.handle}</p>
            <div className="flex gap-4 text-sm mt-1">
              <span>{user.following} Siguiendo</span>
              <span>{user.followers} Seguidores</span>
              <span>{user.outfitsCount} Outfits</span>
            </div>
          </div>
        </div>
        <div className="flex gap-4 mb-4 border-b">
          {tabs.map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`pb-2 ${tab === t ? 'border-b-2 border-black' : ''}`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "outfits" && (
          <div className="grid grid-cols-2 gap-4">
            {looks.map((l) => (
              <img key={l.id} src={l.cover_image} alt={l.title} className="w-full h-40 object-cover rounded" />
            ))}
          </div>
        )}
        {tab === "productos" && (
          <div className="grid grid-cols-2 gap-4">
            {products.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        )}
        {tab === "armario" && (
          <div className="grid grid-cols-2 gap-4">
            {wardrobeProducts.map((p) => (
              <img key={p.id} src={p.images[0]} alt={p.title} className="w-full h-40 object-cover rounded" />
            ))}
          </div>
        )}
        {tab === "pedidos" && (
          <div className="space-y-4">
            {orders.map((o) => (
              <div key={o.id} className="border p-4 rounded">
                <p className="font-semibold">{o.brand}</p>
                <p className="text-sm">{o.title} - Talla {o.size}</p>
                <p className="text-sm">{o.status}</p>
                <p className="text-sm text-gray-500">{o.date}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
