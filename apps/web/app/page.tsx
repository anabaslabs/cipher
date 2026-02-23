"use client";

import Link from "next/link";
import Header from "@/components/Header";
import { Badge } from "@workspace/ui/components/badge";
import { Button } from "@workspace/ui/components/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from "@workspace/ui/components/card";
import Footer from "@/components/Footer";

export default function Home() {
  const playChestOpenSound = () => {
    const audio = new Audio("/chest_open.ogg");
    audio.volume = 0.1;
    audio.play().catch(() => {});
  };

  const features = [
    {
      title: "Encrypt",
      href: "/encrypt",
      description:
        "Secure your text using a custom key. Keeps formatting fully intact.",
    },
    {
      title: "Decrypt",
      href: "/decrypt",
      description:
        "Unlock encrypted text with your key. Recover the original message.",
    },
    {
      title: "Frequency Analysis Attack",
      href: "/attack",
      description:
        "Analyze ciphertext patterns automatically. Reveal likely letter substitutions.",
    },
    {
      title: "Generate Report",
      href: "/report",
      description:
        "Compile insights into a clean summary. Export a ready-to-submit report.",
    },
  ];

  return (
    <>
      <Header animation />
      <main className="flex flex-col justify-evenly items-center gap-8 p-6 min-h-[calc(100vh-9rem)] w-full">
        <div className="flex flex-col justify-center items-center gap-4 text-center max-w-6xl">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
            Your all-in-one toolkit for Cipher Project
          </h1>
          <h2 className="flex flex-wrap justify-center items-center gap-2 font-semibold">
            <span>Supported Ciphers:</span>
            <Badge variant="secondary" className="text-sm border-gray-500">
              Caesar
            </Badge>
            <Badge variant="secondary" className="text-sm border-gray-500">
              Permutation
            </Badge>
            <Badge variant="secondary" className="text-sm border-gray-500">
              Vigenère
            </Badge>
            <Badge variant="secondary" className="text-sm border-gray-500">
              Playfair (8x8)
            </Badge>
            <Badge variant="secondary" className="text-sm border-gray-500">
              Hill (2x2)
            </Badge>
            <Badge variant="secondary" className="text-sm border-gray-500">
              DES
            </Badge>
            <Badge variant="secondary" className="text-sm border-gray-500">
              RC5
            </Badge>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-6xl">
          {features.map((feature) => (
            <Card
              key={feature.title}
              className="flex flex-col justify-between hover:shadow-md transition-shadow"
            >
              <CardHeader>
                <CardTitle>{feature.title}</CardTitle>
                <CardDescription className="mt-1 text-sm">
                  {feature.description}
                </CardDescription>
              </CardHeader>
              <CardFooter>
                <Button variant="default" asChild className="w-full">
                  <Link href={feature.href} onClick={playChestOpenSound}>
                    Open {feature.title}
                  </Link>
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </main>
      <Footer />
    </>
  );
}
