"use client";

export default function Footer() {
  function handleClink(url: string) {
    window.open(url, "_blank", "noopener,noreferrer");
  }

  return (
    <footer className="flex justify-center items-center gap-1.5 text-sm text-muted-foreground py-4">
      <span>Built</span>
      <span>by</span>
      <a
        href="https://github.com/saptarshiroy39"
        target="_blank"
        rel="noopener noreferrer"
        className="underline"
      >
        Saptarshi Roy
      </a>
      <p
        className="underline hover:cursor-pointer"
        onClick={() => handleClink("https://youtu.be/EA4DipdhpV8")}
      >
        &&
      </p>
      <a
        href="https://github.com/itskdhere"
        target="_blank"
        rel="noopener noreferrer"
        className="underline"
      >
        Krishnendu Das
      </a>
    </footer>
  );
}
