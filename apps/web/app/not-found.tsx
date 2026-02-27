"use client";

import { useRouter } from "next/navigation";
import { Button } from "@workspace/ui/components/button";

export default function NotFound() {
  const router = useRouter();

  function handleClick() {
    const audio = new Audio("/faahhh.mp3");
    audio.play().catch(() => {});
    router.push("/");
  }

  return (
    <main
      id="main"
      className="flex flex-col items-center justify-center gap-4 min-h-screen font-lexend"
    >
      <h1 className="text-6xl font-bold">404</h1>
      <h2 className="text-5xl">Not Found</h2>
      <Button
        size="lg"
        variant="outline"
        className="mt-6 text-lg"
        onClick={handleClick}
      >
        Return Home
      </Button>
    </main>
  );
}
