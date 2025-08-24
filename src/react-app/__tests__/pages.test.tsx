import { describe, it, vi } from "vitest";
import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Explore from "../pages/Explore";
import Looks from "../pages/Looks";
import Feed from "../pages/Feed";
import Cart from "../pages/Cart";
import Profile from "../pages/Profile";

vi.mock("@getmocha/users-service/react", () => ({
  useAuth: () => ({ user: { google_user_data: { picture: "" } }, logout: async () => {} }),
  AuthProvider: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

describe("pages render", () => {
  it("renders explore", () => {
    render(
      <MemoryRouter>
        <Explore />
      </MemoryRouter>
    );
  });
  it("renders looks", () => {
    render(
      <MemoryRouter>
        <Looks />
      </MemoryRouter>
    );
  });
  it("renders feed", () => {
    render(
      <MemoryRouter>
        <Feed />
      </MemoryRouter>
    );
  });
  it("renders cart", () => {
    render(
      <MemoryRouter>
        <Cart />
      </MemoryRouter>
    );
  });
  it("renders profile", () => {
    render(
      <MemoryRouter>
        <Profile />
      </MemoryRouter>
    );
  });
});
