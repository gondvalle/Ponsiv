import Layout from "@/react-app/components/Layout";
import { useStore } from "@/shared/store";

export default function Cart() {
  const { cart, updateQuantity, removeFromCart, cartTotal, createOrder } = useStore();

  return (
    <Layout>
      <div className="p-4 pb-32 space-y-4">
        {cart.map((item) => (
          <div key={item.product.id + item.size} className="flex gap-4 items-center">
            <img
              src={item.product.images[0]}
              alt={item.product.title}
              className="w-20 h-20 object-cover rounded"
            />
            <div className="flex-1">
              <p className="font-semibold">{item.product.title}</p>
              <p className="text-sm text-gray-500">Talla {item.size}</p>
              <div className="flex items-center mt-2">
                <button
                  className="px-2 border"
                  onClick={() =>
                    updateQuantity(
                      item.product.id,
                      item.size,
                      Math.max(1, item.quantity - 1)
                    )
                  }
                >
                  -
                </button>
                <span className="px-4">{item.quantity}</span>
                <button
                  className="px-2 border"
                  onClick={() =>
                    updateQuantity(
                      item.product.id,
                      item.size,
                      item.quantity + 1
                    )
                  }
                >
                  +
                </button>
              </div>
            </div>
            <div className="text-right">
              <p>{(item.product.price * item.quantity).toFixed(2)} €</p>
              <button
                className="text-sm text-red-500"
                onClick={() => removeFromCart(item.product.id, item.size)}
              >
                Quitar
              </button>
            </div>
          </div>
        ))}
      </div>
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-4 flex justify-between items-center">
        <span className="font-semibold">
          Total {cartTotal().toFixed(2)} €
        </span>
        <button
          className="bg-[#E6C8A6] px-4 py-2 rounded"
          onClick={createOrder}
        >
          Realizar pedido
        </button>
      </div>
    </Layout>
  );
}
