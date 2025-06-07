import { reserveType } from "./foods.type";

export type userType = {
  id: number;
  email: string;
  fullname: string;
  is_active: boolean;
  is_ban: boolean;
  jlast_login: string;
  last_login: string;
  token: string;
  reserved_foods: reserveType[];
};
