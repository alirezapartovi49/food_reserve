import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const startDate = searchParams.get("start-date");

  const token = req.cookies.get("token")?.value;
  const data = await fetch(startDate ? `${process.env.NEXT_PUBLIC_BACKEND_PATH}/foods/week-foods?start-date=${startDate}` : `${process.env.NEXT_PUBLIC_BACKEND_PATH}/foods/week-foods`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }).then((res) => res.json());

  return NextResponse.json({ data });
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const token = req.cookies.get("token")?.value;

  const reserveFood = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_PATH}/reserve/reserve`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  });

  return NextResponse.json({ reserveFood }, { status: reserveFood.status });
}
