// app/api/estado/[id]/route.ts
import { NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export async function GET(request: Request, { params }: { params: { id: string } }) {
  const { id } = params;

  const estado = await prisma.estado.findUnique({
    where: { id: Number(id) },
    include: { primavera: true, verano: true, otonio: true, invierno: true },
  });

  if (!estado) return NextResponse.json({ error: "Estado no encontrado" }, { status: 404 });

  return NextResponse.json(estado);
}
