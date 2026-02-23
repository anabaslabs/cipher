"use client";

import { useEffect } from "react";
import { formatBytes, useFileUpload } from "@/hooks/use-file-upload";
import { Button } from "@workspace/ui/components/button";
import { cn } from "@workspace/ui/lib/utils";
import {
  IconFilePlus,
  IconFileTypeTxt,
  IconFileUnknown,
  IconAlertCircle,
  IconTrash,
} from "@tabler/icons-react";

export type State = "idle" | "processing" | "done" | "error";

export default function FileSelector({
  className,
  titleText,
  state,
  setFile,
  onClearFilesReady,
}: {
  className?: string;
  titleText?: string;
  state: State;
  setFile: (file: File | null) => void;
  onClearFilesReady?: (clearFiles: () => void) => void;
}) {
  const [
    { files, isDragging, errors },
    {
      handleDragEnter,
      handleDragLeave,
      handleDragOver,
      handleDrop,
      openFileDialog,
      clearFiles,
      getInputProps,
    },
  ] = useFileUpload({
    multiple: false,
    accept: "text/plain",
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10 MB
  });

  useEffect(() => {
    if (files.length > 0 && files[0]?.file instanceof File) {
      setFile(files[0].file);
    } else {
      setFile(null);
    }
  }, [files, setFile]);

  useEffect(() => {
    if (onClearFilesReady) {
      onClearFilesReady(clearFiles);
    }
  }, [onClearFilesReady, clearFiles]);

  return (
    <div className={cn("flex flex-col gap-4", className)}>
      <div
        role="button"
        onClick={openFileDialog}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        data-dragging={isDragging || undefined}
        className="flex flex-col items-center justify-center rounded-lg border border-dashed border-input p-4 transition-colors hover:cursor-cell hover:bg-accent/50 has-disabled:pointer-events-none has-disabled:opacity-50 has-[input:focus]:border-ring has-[input:focus]:ring-[3px] has-[input:focus]:ring-ring/50 data-[dragging=true]:bg-accent/50"
      >
        <input
          {...getInputProps()}
          className="sr-only"
          aria-label="Select file"
          disabled={state !== "idle"}
        />

        <div className="flex flex-col items-center justify-center text-center">
          <div
            className="mb-2 flex size-12 shrink-0 items-center justify-center border rounded-full bg-background"
            aria-hidden="true"
          >
            <IconFilePlus className="size-6 opacity-60" />
          </div>
          <p className="mb-1.5 text-lg font-medium">
            {titleText || "Add File"}
          </p>
          <p className="mb-2 text-muted-foreground">
            Drag & Drop / Click to browse file
          </p>
          <div className="flex flex-wrap justify-center gap-1 text-sm text-muted-foreground/70">
            <span>Only Text (.txt) file</span>
            <span> • </span>
            <span>Size upto 10MB</span>
          </div>
        </div>
      </div>

      {errors.length > 0 && (
        <div
          className="flex items-center gap-1 text-xs text-destructive"
          role="alert"
        >
          <IconAlertCircle className="size-3 shrink-0" />
          <span>{errors[0]}</span>
        </div>
      )}

      <div className="space-y-2">
        <div
          key={files[0]?.id}
          className="flex items-center justify-between gap-2 rounded-lg border p-2 pe-3"
        >
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="flex aspect-square size-12 shrink-0 items-center justify-center rounded border">
              {files[0]?.file instanceof File ? (
                <IconFileTypeTxt
                  className="size-6 opacity-70"
                  aria-hidden="true"
                />
              ) : (
                <IconFileUnknown
                  className="size-6 opacity-70"
                  aria-hidden="true"
                />
              )}
            </div>
            <div className="flex min-w-0 flex-col gap-0.5">
              <p
                className="truncate text-sm font-medium"
                title={
                  files[0]?.file instanceof File
                    ? files[0].file.name
                    : "No file selected"
                }
              >
                {files[0]?.file instanceof File
                  ? files[0].file.name
                  : "No file selected"}
              </p>
              <div className="flex flex-wrap justify-start gap-1 text-xs text-muted-foreground">
                <span>
                  {formatBytes(
                    files[0]?.file instanceof File ? files[0].file.size : 0
                  )}
                </span>
              </div>
            </div>
          </div>

          <Button
            size="icon"
            variant="ghost"
            className="-me-2 size-8 text-muted-foreground/80 hover:bg-transparent hover:text-foreground hover:cursor-pointer"
            onClick={clearFiles}
            disabled={files.length === 0 || state !== "idle"}
            aria-label="Remove file"
          >
            <IconTrash className="size-4.5 text-red-400" aria-hidden="true" />
          </Button>
        </div>
      </div>
    </div>
  );
}
