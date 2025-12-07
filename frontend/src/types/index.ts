export interface User {
  id: number;
  email: string;
  username: string;
  telegram_username?: string;
  phone?: string;
  createdAt: string;
}

export interface AuthResponse {
  id: number;
  username: string;
  email: string;
  telegram_username?: string;
  session_token: string;
  message: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  username: string;
  telegram_username?: string;
  phone?: string;
}

export enum PerfumeType {
  FLORAL = "floral",
  WOODY = "woody",
  ORIENTAL = "oriental",
  FRESH = "fresh",
  CITRUS = "citrus",
  GOURMAND = "gourmand",
  AQUATIC = "aquatic",
  CHYPRE = "chypre",
  FOUGERE = "fougere"
}

export interface Perfume {
  id: number;
  name: string;
  brand: string;
  price: number;
  perfume_type: PerfumeType;
  description?: string;
  img_url?: string;
  stock_quantity: number;
  volume: number;
  concentration: string;
}

export interface CartItem {
  id: number;
  order_id: number;
  perfume: Perfume;
  quantity: number;
  price: number;
}

export interface Cart {
  id: number;
  userName: string;
  userPhone: string;
  totalAmount: number;
  status: string;
  createdAt: string;
  confirmedAt: string;
  items: CartItem[];
}

export interface OrderItem {
  id: number;
  perfume_id: number;
  quantity: number;
  price: number;
}

export interface Order {
  id: number;
  status: string;
  items: OrderItem[];
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}