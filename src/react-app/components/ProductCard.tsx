import { Product } from "@/shared/types";

interface Props {
  product: Product;
}

export default function ProductCard({ product }: Props) {
  return (
    <div className="border rounded-lg overflow-hidden shadow-sm">
      <img
        src={product.images[0]}
        alt={product.title}
        className="w-full h-40 object-cover"
      />
      <div className="p-2 text-sm">
        <p className="font-semibold">{product.title}</p>
        <p className="text-gray-500">{product.brand}</p>
        <p className="font-medium">{product.price.toFixed(2)} €</p>
      </div>
    </div>
  );
}
