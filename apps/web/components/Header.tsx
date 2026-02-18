"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@workspace/ui/components/button";
import { AnimatedThemeToggler } from "@workspace/ui/components/animated-theme-toggler";
import { IconArrowLeft } from "@tabler/icons-react";

export default function Header({
  backButton = false,
  titleText,
}: {
  backButton?: boolean;
  titleText?: string;
}) {
  const router = useRouter();

  return (
    <header className="flex justify-center items-center px-4 sm:px-6 py-4 w-full">
      <div className="flex justify-between items-center w-full max-w-6xl">
        <h1 className="flex justify-center items-center gap-2 text-2xl font-bold">
          {backButton && (
            <Button
              size="icon"
              variant="secondary"
              className="rounded-full p-px"
              onClick={() => router.back()}
              aria-label="Go back"
            >
              <IconArrowLeft className="size-5" aria-hidden="true" />
            </Button>
          )}
          <span>{titleText || "CNS Solver"}</span>
        </h1>
        <AnimatedThemeToggler className="p-1 border rounded-full bg-accent hover:bg-accent/70" />
      </div>
    </header>
  );
}
