import Layout from "@/react-app/components/Layout";
import ProductCard from "@/react-app/components/ProductCard";
import { useStore } from "@/shared/store";

export default function Explore() {
  const { products } = useStore();
  return (
    <Layout>
      <div className="p-4">
        <input
          type="text"
          placeholder="Buscar marcas, estilos o prendas…"
          className="w-full p-2 border rounded mb-4"
        />
        <h2 className="text-xl font-semibold mb-2">Tendencias del momento</h2>
        <div className="grid grid-cols-2 gap-4">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </div>
    </Layout>
  );
}
