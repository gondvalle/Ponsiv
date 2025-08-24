import Layout from "@/react-app/components/Layout";
import ProductCard from "@/react-app/components/ProductCard";
import { useStore } from "@/shared/store";

export default function Feed() {
  const { products } = useStore();
  return (
    <Layout>
      <div className="h-screen overflow-y-scroll snap-y snap-mandatory">
        {products.map((p) => (
          <div key={p.id} className="snap-start h-screen">
            <ProductCard product={p} />
          </div>
        ))}
      </div>
    </Layout>
  );
}
