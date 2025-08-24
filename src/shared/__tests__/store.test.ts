import { describe, it, expect } from "vitest";
import { useStore } from "../store";
import { act } from "@testing-library/react";

describe("store cart", () => {
  it("calculates total correctly", () => {
    const { products, addToCart, cartTotal } = useStore.getState();
    act(() => {
      addToCart(products[0], "M");
      addToCart(products[0], "M");
    });
    expect(cartTotal()).toBeCloseTo(products[0].price * 2);
  });
});
