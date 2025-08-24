import Layout from "@/react-app/components/Layout";
import { useStore } from "@/shared/store";

export default function Looks() {
  const { looks } = useStore();
  return (
    <Layout>
      <div className="p-4 grid grid-cols-2 gap-4">
        {looks.map((l) => (
          <div key={l.id} className="border rounded-lg overflow-hidden">
            <img src={l.cover_image} alt={l.title} className="w-full h-40 object-cover" />
            <div className="p-2 text-sm">
              <p className="font-semibold">{l.title}</p>
              <p className="text-gray-500">Por {l.author.name}</p>
            </div>
          </div>
        ))}
      </div>
    </Layout>
  );
}
