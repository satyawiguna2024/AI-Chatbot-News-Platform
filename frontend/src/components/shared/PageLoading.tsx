import IconLoading from "@/assets/icons/icon-loading.png"

export default function PageLoading() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="flex flex-col items-center gap-3">
        <img src={IconLoading} alt="Loading..." className="size-32 animate-spin" />
      </div>
    </div>
  );
}
