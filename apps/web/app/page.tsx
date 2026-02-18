import Link from "next/link";
import Header from "@/components/Header";
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
      <main className="flex flex-col justify-center items-center p-6 min-h-[calc(100vh-8rem)] w-full">
        <div className="text-center mt-2 mb-14 max-w-6xl">
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
            Your all-in-one toolkit for Cipher Project
          </h1>
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
                  <Link href={feature.href}>Open {feature.title}</Link>
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
