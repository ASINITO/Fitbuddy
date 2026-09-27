// FitBuddy Global JavaScript Utilities
console.log("FitBuddy AI Fitness Platform initialized.");

// Global Toast or Notification display
function showToast(message, type = "success") {
    const toast = document.createElement("div");
    const bgClass = type === "success" ? "bg-emerald-500 text-slate-950" : "bg-red-500 text-white";
    toast.className = `fixed bottom-5 right-5 z-50 px-4 py-2.5 rounded-xl shadow-2xl font-bold text-xs flex items-center gap-2 ${bgClass} transition-all duration-300`;
    toast.innerHTML = `<span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
