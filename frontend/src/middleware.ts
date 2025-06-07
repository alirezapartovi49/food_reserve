import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

async function middleware(req: NextRequest) {
  const url = req.nextUrl;
  const cookiesHeader = await cookies();
  const token = cookiesHeader.get("token");

  if (url.pathname === "/" || url.pathname === "/reserve") {
    if (!token) {
      return NextResponse.redirect(new URL("/login", url));
    }
  } else if (url.pathname === "/login") {
    if (token) {
      return NextResponse.redirect(new URL("/", url));
    }
  }
  return NextResponse.next();
}

export default middleware;
