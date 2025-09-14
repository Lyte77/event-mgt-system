
  const navbar = document.getElementById("navbar");
  const menuToggle = document.getElementById("menuToggle");
  const mobileMenu = document.getElementById("mobileMenu");
  const menuIcon = document.getElementById("menuIcon");
  const closeIcon = document.getElementById("closeIcon");
  const scrollTopBtn = document.getElementById("scrollTopBtn");

  // Change navbar style on scroll
  // window.addEventListener("scroll", () => {
  //   if (window.scrollY > 10) {
  //     navbar.classList.add("bg-white/80", "backdrop-blur-md", "shadow-sm");
  //     navbar.classList.remove("bg-transparent");
  //   } else {
  //     navbar.classList.remove("bg-white/80", "backdrop-blur-md", "shadow-sm");
  //     navbar.classList.add("bg-transparent");
  //   }
  // });

  // Toggle mobile menu
  menuToggle.addEventListener("click", () => {
    const isOpen = !mobileMenu.classList.contains("translate-x-full");
    if (isOpen) {
      mobileMenu.classList.add("opacity-0", "translate-x-full", "pointer-events-none");
      menuIcon.classList.remove("hidden");
      closeIcon.classList.add("hidden");
      document.body.style.overflow = "";
    } else {
      mobileMenu.classList.remove("opacity-0", "translate-x-full", "pointer-events-none");
      menuIcon.classList.add("hidden");
      closeIcon.classList.remove("hidden");
      document.body.style.overflow = "hidden";
    }
  });

  // Smooth scroll to top
  scrollTopBtn.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
    mobileMenu.classList.add("opacity-0", "translate-x-full", "pointer-events-none");
    menuIcon.classList.remove("hidden");
    closeIcon.classList.add("hidden");
    document.body.style.overflow = "";
  });

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



function dashboard(){
    return {
      sidebarOpen: false,
      profileModal: false,
      pastOpen: true,
      ticketFilter: 'all',
      ticketModal: { open: false, id: null },
      feedbackModal: { open: false, eventId: null, title: '' },

      openTicketModal(id){
        this.ticketModal.id = id;
        this.ticketModal.open = true;
      },
      closeTicketModal(){
        this.ticketModal.open = false;
        this.ticketModal.id = null;
      },

      openProfileModal(){ this.profileModal = true; },
      openFeedbackModal(id, title){
        this.feedbackModal.eventId = id;
        this.feedbackModal.title = title;
        this.feedbackModal.open = true;
      },
      closeFeedbackModal(){
        this.feedbackModal = { open: false, eventId: null, title: '' };
      },

      matchesFilter(scope, filter){
        if(filter === 'all') return true;
        return scope === filter;
      }
    }
  }

  // Follow HX-Redirect header for downloads
  document.body.addEventListener('htmx:afterOnLoad', (evt) => {
    const redirect = evt.detail.xhr.getResponseHeader('HX-Redirect');
    if (redirect) window.location.href = redirect;
  });