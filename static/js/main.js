// Animate numbers on scroll
  function animateCounter(el, target) {
    let start = 0;
    let duration = 2000;
    let stepTime = Math.abs(Math.floor(duration / target));
    let timer = setInterval(() => {
      start += 1;
      el.textContent = start.toLocaleString();
      if (start >= target) clearInterval(timer);
    }, stepTime);
  }

  // Observer to trigger when stats are visible
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        animateCounter(el, parseInt(el.dataset.target));
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll("#stats dd").forEach(stat => {
    observer.observe(stat);
  });

//how it works animation

  // Animate steps when scrolled into view
  document.addEventListener("DOMContentLoaded", () => {
    const steps = document.querySelectorAll(".how-step");
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.remove("opacity-0", "translate-y-8");
          entry.target.classList.add("opacity-100", "translate-y-0");
          observer.unobserve(entry.target); // animate once
        }
      });
    }, { threshold: 0.2 });

    steps.forEach(step => observer.observe(step));
  });