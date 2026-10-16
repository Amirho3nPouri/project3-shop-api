// ==================== PhemaPlant Main JS ====================

// ==================== Lenis Smooth Scroll ====================
(function () {
  if (typeof Lenis === "undefined") return;

  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    direction: "vertical",
    gestureDirection: "vertical",
    smooth: true,
    mouseMultiplier: 1,
    smoothTouch: false,
    touchMultiplier: 2,
    infinite: false,
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  window.lenis = lenis;

  // برای لینک‌های anchor
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const href = this.getAttribute("href");
      if (href === "#") return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        lenis.scrollTo(target, { offset: -100, duration: 1.5 });
      }
    });
  });
})();

// ==================== Dark Mode Toggle ====================
(function () {
  const themeToggle = document.getElementById("theme-toggle");
  const themeToggleMobile = document.getElementById("theme-toggle-mobile");
  const html = document.documentElement;

  const currentTheme = localStorage.getItem("theme") || "light";
  if (currentTheme === "dark") {
    html.classList.add("dark");
  }

  function toggleTheme(iconId) {
    html.classList.toggle("dark");
    const newTheme = html.classList.contains("dark") ? "dark" : "light";
    localStorage.setItem("theme", newTheme);

    const icon = document.getElementById(iconId);
    if (icon) {
      icon.style.transform = "rotate(360deg)";
      setTimeout(() => {
        icon.style.transform = "rotate(0deg)";
      }, 700);
    }
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", () => toggleTheme("sunflower-icon"));
  }

  if (themeToggleMobile) {
    themeToggleMobile.addEventListener("click", () =>
      toggleTheme("sunflower-icon-mobile"),
    );
  }
})();

// ==================== Mobile Menu ====================
(function () {
  const menuBtn = document.getElementById("mobile-menu-btn");
  const menu = document.getElementById("mobile-menu");
  const menuDrawer = document.getElementById("mobile-menu-drawer");
  const menuClose = document.getElementById("mobile-menu-close");
  const menuBackdrop = document.getElementById("mobile-menu-backdrop");

  if (!menuBtn || !menu) return;

  function openMenu() {
    menu.classList.remove("hidden");
    setTimeout(() => {
      menuDrawer.classList.remove("translate-x-full");
    }, 10);
    document.body.style.overflow = "hidden";
    if (window.lenis) window.lenis.stop();
  }

  function closeMenu() {
    menuDrawer.classList.add("translate-x-full");
    setTimeout(() => {
      menu.classList.add("hidden");
    }, 300);
    document.body.style.overflow = "";
    if (window.lenis) window.lenis.start();
  }

  menuBtn.addEventListener("click", openMenu);
  if (menuClose) menuClose.addEventListener("click", closeMenu);
  if (menuBackdrop) menuBackdrop.addEventListener("click", closeMenu);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !menu.classList.contains("hidden")) {
      closeMenu();
    }
  });
})();

// ==================== Cart Count ====================
window.updateCartCount = function () {
  const cartCount = document.getElementById("cart-count");
  if (!cartCount) return;

  const token = localStorage.getItem("access_token");
  if (!token) {
    cartCount.classList.add("hidden");
    return;
  }

  fetch("/api/cart/my_cart/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.total_items > 0) {
        cartCount.textContent = data.total_items;
        cartCount.classList.remove("hidden");
      } else {
        cartCount.classList.add("hidden");
      }
    })
    .catch(() => {
      cartCount.classList.add("hidden");
    });
};

window.updateCartCount();

// ==================== Toast Notification ====================
window.showToast = function (message, type = "success") {
  const existingToast = document.querySelector(".phema-toast");
  if (existingToast) existingToast.remove();

  const toast = document.createElement("div");
  toast.className = `phema-toast fixed bottom-6 left-1/2 -translate-x-1/2 px-6 py-3 rounded-xl shadow-lg text-white font-medium z-[10000] transition-all duration-300 ${
    type === "success" ? "bg-phema-green" : "bg-red-500"
  }`;
  toast.textContent = message;
  toast.style.opacity = "0";
  toast.style.transform = "translate(-50%, 20px)";

  document.body.appendChild(toast);

  requestAnimationFrame(() => {
    toast.style.opacity = "1";
    toast.style.transform = "translate(-50%, 0)";
  });

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translate(-50%, 20px)";
    setTimeout(() => toast.remove(), 300);
  }, 2500);
};

// ==================== Add to Cart Animation v2 ====================
window.addToCartAnimated = async function (
  productId,
  buttonElement,
  quantity = 1,
) {
  const token = localStorage.getItem("access_token");

  if (!token) {
    window.location.href = "/login/";
    return false;
  }

  const btn = buttonElement;

  if (
    btn.classList.contains("animating") ||
    btn.classList.contains("success")
  ) {
    return false;
  }

  btn.classList.add("animating");

  const btnText = btn.querySelector(".btn-text");
  const originalHTML = btnText ? btnText.innerHTML : "";

  try {
    const response = await fetch("/api/cart/add/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        product_id: productId,
        quantity: quantity,
      }),
    });

    setTimeout(() => {
      btn.classList.remove("animating");

      if (response.ok) {
        btn.classList.add("success");

        if (btnText) {
          btnText.innerHTML = "✅ اضافه شد";
        }

        if (window.updateCartCount) window.updateCartCount();

        const cartIcon = document.querySelector('a[href="/cart/"]');
        if (cartIcon) {
          cartIcon.classList.add("animate-bounce");
          setTimeout(() => cartIcon.classList.remove("animate-bounce"), 600);
        }

        window.showToast(`✅ ${quantity} عدد به سبد اضافه شد!`, "success");

        setTimeout(() => {
          btn.classList.remove("success");
          if (btnText) btnText.innerHTML = originalHTML;
        }, 2000);
      } else {
        response
          .json()
          .then((data) => {
            window.showToast("❌ " + (data.error || "خطایی رخ داد"), "error");
          })
          .catch(() => {
            window.showToast("❌ خطایی رخ داد", "error");
          });
      }
    }, 1800);

    return response.ok;
  } catch (error) {
    setTimeout(() => {
      btn.classList.remove("animating");
      window.showToast("❌ خطای شبکه", "error");
    }, 1800);
    return false;
  }
};

// ==================== Back to Top ====================
(function () {
  const btn = document.getElementById("back-to-top");
  if (!btn) return;

  function checkScroll() {
    if (window.scrollY > 400) {
      btn.classList.remove("opacity-0", "pointer-events-none");
      btn.classList.add("opacity-100");
    } else {
      btn.classList.add("opacity-0", "pointer-events-none");
      btn.classList.remove("opacity-100");
    }
  }

  window.addEventListener("scroll", checkScroll);
  checkScroll();

  btn.addEventListener("click", () => {
    if (window.lenis) {
      window.lenis.scrollTo(0, { duration: 1.5 });
    } else {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  });
})();

// ==================== Skeleton Generators ====================
window.createProductSkeleton = function () {
  return `
        <div class="skeleton-card">
            <div class="skeleton skeleton-image"></div>
            <div class="p-5">
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text skeleton-text-sm"></div>
                <div class="flex justify-between items-center mt-4">
                    <div class="skeleton skeleton-text" style="width: 40%;"></div>
                    <div class="skeleton" style="width: 40px; height: 40px; border-radius: 50%;"></div>
                </div>
            </div>
        </div>
    `;
};

window.createCategorySkeleton = function () {
  return `
        <div class="skeleton-card">
            <div class="skeleton skeleton-image"></div>
            <div class="p-5 text-center">
                <div class="skeleton skeleton-text" style="width: 70%; margin: 0 auto 8px;"></div>
                <div class="skeleton skeleton-text skeleton-text-sm" style="margin: 0 auto;"></div>
            </div>
        </div>
    `;
};

window.createOrderSkeleton = function () {
  return `
        <div class="skeleton-card p-6">
            <div class="flex justify-between items-center mb-4">
                <div style="flex: 1;">
                    <div class="skeleton skeleton-title" style="width: 40%;"></div>
                    <div class="skeleton skeleton-text" style="width: 30%;"></div>
                </div>
                <div class="skeleton skeleton-text" style="width: 25%;"></div>
            </div>
            <div class="border-t border-phema-text/5 dark:border-phema-gold/10 pt-4">
                <div class="skeleton skeleton-text mb-2"></div>
                <div class="skeleton skeleton-text" style="width: 80%;"></div>
            </div>
        </div>
    `;
};

// ==================== Scroll Progress Bar ====================
(function () {
  const progressBar = document.getElementById("scroll-progress");
  if (!progressBar) return;

  function updateProgress() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight =
      document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = progress + "%";
  }

  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress, { passive: true });
  updateProgress();
})();

// ==================== Reveal on Scroll ====================
(function () {
  // به‌طور خودکار به بخش‌های اصلی کلاس reveal اضافه کن
  const sections = document.querySelectorAll("section");

  sections.forEach((section, index) => {
    if (
      section.classList.contains("reveal") ||
      section.classList.contains("reveal-right") ||
      section.classList.contains("reveal-left") ||
      section.classList.contains("reveal-scale")
    ) {
      return;
    }

    if (index > 0) {
      section.classList.add("reveal");
    }
  });

  const reveals = document.querySelectorAll(
    ".reveal, .reveal-right, .reveal-left, .reveal-scale",
  );

  if (reveals.length === 0) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("active");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: "0px 0px -80px 0px",
    },
  );

  reveals.forEach((el) => observer.observe(el));
})();

// ==================== Parallax on Scroll ====================
(function () {
  const parallaxElements = document.querySelectorAll(".parallax");
  if (parallaxElements.length === 0) return;

  let ticking = false;

  function updateParallax() {
    const scrollY = window.scrollY;

    parallaxElements.forEach((el) => {
      const speed = parseFloat(el.dataset.speed) || 0.5;
      const offset = scrollY * speed;
      el.style.transform = `translateY(${offset}px)`;
    });

    ticking = false;
  }

  window.addEventListener(
    "scroll",
    () => {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    },
    { passive: true },
  );
})();
