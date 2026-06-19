document.addEventListener('alpine:init', () => {
  Alpine.data('adminState', () => ({
    currentTab: 'dashboard',
    sidebarOpen: true,
    notifications: [],
    
    // Search & Filter state
    searchQueries: {
      applications: '',
      users: '',
      events: '',
      validators: ''
    },
    filters: {
      applications: 'all', // 'all', 'Pending', 'Approved', 'Rejected'
      users: 'all',        // 'all', 'Attendee', 'Organizer', 'Admin', 'Suspended'
      events: 'all'        // 'all', 'Active', 'Disabled', 'Registration Closed'
    },

    // Modals
    modals: {
      reject: { show: false, targetId: null, reason: '' },
      editEvent: { show: false, targetId: null, title: '', date: '', status: '', attendeesCount: 0, organizer: '' },
      attendees: { show: false, targetEventId: null, query: '' },
      assignValidator: { show: false, targetId: null, selectedEvent: '' }
    },

    // Selected Expanded application IDs
    expandedApplications: [],

    // Mock Databases (State-mutators work directly on these)
    applications: [
      {
        id: 1,
        userName: 'Sarah Connor',
        email: 'sarah@technovation.io',
        orgName: 'TechNovation Events',
        country: 'United States',
        date: '2026-06-12',
        status: 'Pending',
        avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
        reason: 'We want to host our annual Vanguard Developer Summit for 1,500+ attendees. Seeking high-concurrency ticket validation and platform monitoring to track real-time entry ratios.',
        experience: '8+ years coordinating regional scale tech meetups and hackathons across North America.',
        rejectionReason: ''
      },
      {
        id: 2,
        userName: 'Aris Thorne',
        email: 'thorne@elysium.ca',
        orgName: 'Elysium Sound Forests',
        country: 'Canada',
        date: '2026-06-11',
        status: 'Pending',
        avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
        reason: 'Curating an upcoming eco-conscious midsummer sound and light sanctuary. Requires ticket validation networks across 3 remote, cellular-challenged forest gates.',
        experience: 'Promoting independent musical events and woodland showcases across British Columbia since 2019.',
        rejectionReason: ''
      },
      {
        id: 3,
        userName: 'Kofi Mensah',
        email: 'kofi@greeninitiative.org',
        orgName: 'Global Green Initiative',
        country: 'Ghana',
        date: '2026-06-08',
        status: 'Approved',
        avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
        reason: 'Developing international summits on urban architectural agricultural systems.',
        experience: 'Educational and civic organizer for governmental panels and green energy groups across West Africa.',
        rejectionReason: ''
      },
      {
        id: 4,
        userName: 'Elena Rostova',
        email: 'elena@whitenights.co.uk',
        orgName: 'White Nights Classical',
        country: 'United Kingdom',
        date: '2026-06-10',
        status: 'Pending',
        avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
        reason: 'Providing high-end open-air classical recitals under the midsummer sky. Demands multiple check-in queues for VIP tier ticket owners.',
        experience: 'Former artistic director for Manchester Concert Hall; hosting boutique outdoor orchestral showcases.',
        rejectionReason: ''
      },
      {
        id: 5,
        userName: 'Mateo Rivera',
        email: 'rivera@apexevents.mx',
        orgName: 'Apex Sports Summit',
        country: 'Mexico',
        date: '2026-06-05',
        status: 'Rejected',
        avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
        reason: 'Casual block parties and local beach soccer invitationals in CDMX.',
        experience: 'Local coordinator for recreational youth leagues.',
        rejectionReason: 'Invalid corporate liability registry and insufficient host licensing data provided.'
      }
    ],

    users: [
      { id: 101, name: 'Kofi Mensah', email: 'kofi@greeninitiative.org', role: 'Organizer', status: 'Active', eventsCount: 3, lastLogin: '2 mins ago', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80' },
      { id: 102, name: 'Sarah Connor', email: 'sarah@technovation.io', role: 'Attendee', status: 'Active', eventsCount: 0, lastLogin: '1 hour ago', avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80' },
      { id: 103, name: 'Aris Thorne', email: 'thorne@elysium.ca', role: 'Attendee', status: 'Active', eventsCount: 0, lastLogin: '5 mins ago', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80' },
      { id: 104, name: 'Elena Rostova', email: 'elena@whitenights.co.uk', role: 'Attendee', status: 'Active', eventsCount: 0, lastLogin: '12 hours ago', avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80' },
      { id: 105, name: 'Mateo Rivera', email: 'rivera@apexevents.mx', role: 'Attendee', status: 'Suspended', eventsCount: 0, lastLogin: '1 week ago', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80' },
      { id: 106, name: 'Jane Cooper', email: 'jane.c@validators.io', role: 'Validator', status: 'Active', eventsCount: 1, lastLogin: '10 mins ago', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80' },
      { id: 107, name: 'Devon Lane', email: 'devon.l@validators.io', role: 'Validator', status: 'Active', eventsCount: 1, lastLogin: '3 mins ago', avatar: 'https://images.unsplash.com/photo-1519345182560-3f2917c472ef?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80' },
      { id: 108, name: 'Platform Admin', email: 'admin@vanguard.io', role: 'Admin', status: 'Active', eventsCount: 0, lastLogin: 'Just now', avatar: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80' }
    ],

    events: [
      { id: 201, title: 'Vanguard Developer Conference 2026', organizer: 'Kofi Mensah', date: '2026-07-15', status: 'Active', attendeesCount: 420, capacity: 500, desc: 'The annual regional forum for systems designers, devops teams, and web architects.' },
      { id: 202, title: 'Elysium Sound Forests Sanctuary', organizer: 'Aris Thorne', date: '2026-08-01', status: 'Disabled', attendeesCount: 852, capacity: 1200, desc: 'An deep eco-festival highlighting underground ambient composers power by battery assets.' },
      { id: 203, title: 'Sustainable Cities Symposia', organizer: 'Kofi Mensah', date: '2026-09-10', status: 'Active', attendeesCount: 145, capacity: 300, desc: 'Integrating urban designers, foresters, and civic leaders to structure vertical greenery.' },
      { id: 204, title: 'CDMX Rooftop Block Party', organizer: 'Mateo Rivera', date: '2026-06-25', status: 'Disabled', attendeesCount: 0, capacity: 150, desc: 'Techno social gatherings overlooking the historic CDMX skylit horizon.' },
      { id: 205, title: 'Global Agriculture Workshop', organizer: 'Kofi Mensah', date: '2026-06-20', status: 'Registration Closed', attendeesCount: 50, capacity: 50, desc: 'Hands-on practice in soil chemistry, hydroponics setups, and urban backyard planting.' }
    ],

    validators: [
      { id: 301, name: 'Devon Lane', email: 'devon.l@validators.io', assignedEvents: ['Vanguard Developer Conference 2026'], status: 'Active', avatar: 'https://images.unsplash.com/photo-1519345182560-3f2917c472ef?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80', logsCount: 14 },
      { id: 302, name: 'Jane Cooper', email: 'jane.c@validators.io', assignedEvents: ['Global Agriculture Workshop'], status: 'Active', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80', logsCount: 31 },
      { id: 303, name: 'Esther Howard', email: 'esther.h@validators.io', assignedEvents: ['Sustainable Cities Symposia'], status: 'Active', avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80', logsCount: 22 },
      { id: 304, name: 'Albert Flores', email: 'albert.f@validators.io', assignedEvents: [], status: 'Inactive', avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80', logsCount: 0 }
    ],

    // Global Activity Logs
    activityFeed: [
      { id: 1, time: '3 mins ago', text: 'Devon Lane validated Ticket #B8E42 for Attendee Marcus Aurelius', type: 'validation' },
      { id: 2, time: '14 mins ago', text: 'Jane Cooper scanned Ticket #F1A30 for Attendee Sarah Connor', type: 'validation' },
      { id: 3, time: '1 hour ago', text: 'New organizer application submitted by Sarah Connor (TechNovation Events)', type: 'application' },
      { id: 4, time: '4 hours ago', text: 'System diagnostics auto-checked: Platform load 2.1% - Healthy', type: 'system' }
    ],

    // Analytics Dashboard Details
    hoveredGrowthPoint: { month: 'Jun 2026', total: '11,450 Users', delta: '+34% MoM' },
    hoveredEventsPoint: { week: 'Week 4', count: '31 Events', fill: '#ff5500' },

    // Platform Level Settings
    settings: {
      emailStatus: 'Syncing',
      maintenanceMode: false,
      instantApproval: false,
      emailVerification: true,
      defaultAttendeeStatus: 'Active',
      defaultOrganizerStatus: 'Pending',
      securityLevel: 'Standard Enterprise'
    },

    // Interactive Alerts Count
    alertCount: 1,
    showAlertBanner: true,

    // Real-Time Time
    currentTime: '2026-06-12T15:49:18-07:00',

    init() {
      // Keep digital clock updating representing platform activity
      setInterval(() => {
        let d = new Date();
        this.currentTime = d.toLocaleString();
      }, 1000);
      
      this.triggerToast('Welcome, Administrator. Session authorized securely.', 'success');
    },

    // Helper: Dynamic KPI computation
    get kpi() {
      return {
        totalUsers: this.users.length + 8420, // Offset to show real scale
        activeOrganizers: this.users.filter(u => u.role === 'Organizer' && u.status === 'Active').length,
        pendingApps: this.applications.filter(a => a.status === 'Pending').length,
        totalEvents: this.events.length + 112,
        ticketsIssued: 14240,
        todayCheckins: this.validators.reduce((sum, v) => sum + v.logsCount, 0) + 128
      };
    },

    // Toast triggers
    triggerToast(message, type = 'success') {
      const id = Date.now();
      this.notifications.push({ id, message, type });
      setTimeout(() => {
        this.notifications = this.notifications.filter(n => n.id !== id);
      }, 5000);
    },

    // Feed logger helper
    logActivity(text, type = 'system') {
      this.activityFeed.unshift({
        id: Date.now(),
        time: 'Just now',
        text,
        type
      });
    },

    // Expand Organizer detail trigger
    toggleApplicationExpand(id) {
      if (this.expandedApplications.includes(id)) {
        this.expandedApplications = this.expandedApplications.filter(x => x !== id);
      } else {
        this.expandedApplications.push(id);
      }
    },

    // Organizer Approvals workflows
    approveApplication(id) {
      const app = this.applications.find(a => a.id === id);
      if (app) {
        app.status = 'Approved';
        
        // Ensure user account is promoted to Organizer roles
        const existingUser = this.users.find(u => u.email === app.email);
        if (existingUser) {
          existingUser.role = 'Organizer';
          existingUser.status = 'Active';
        } else {
          this.users.unshift({
            id: Number('12' + id),
            name: app.userName,
            email: app.email,
            role: 'Organizer',
            status: 'Active',
            eventsCount: 0,
            lastLogin: 'Never',
            avatar: app.avatar
          });
        }
        this.triggerToast(`Organizer application for "${app.orgName}" APPROVED successfully.`, 'success');
        this.logActivity(`Approved organizer credentials for "${app.userName}" (${app.orgName})`, 'application');
      }
    },

    // Trigger Rejection workflow using custom overlay modal
    openRejectModal(id) {
      this.modals.reject.targetId = id;
      this.modals.reject.reason = '';
      this.modals.reject.show = true;
    },

    submitRejection() {
      const id = this.modals.reject.targetId;
      const reason = this.modals.reject.reason.trim();
      if (!reason) {
        this.triggerToast('A rejection description matches operational standards and must be specified.', 'error');
        return;
      }
      
      const app = this.applications.find(a => a.id === id);
      if (app) {
        app.status = 'Rejected';
        app.rejectionReason = reason;

        // Revoke organizer authorization if exists
        const userObj = this.users.find(u => u.email === app.email);
        if (userObj) {
          userObj.role = 'Attendee';
        }

        this.triggerToast(`Rejected application for "${app.orgName}". Reason logged.`, 'warning');
        this.logActivity(`Rejected application for "${app.userName}" (${app.orgName}). Reason: ${reason}`, 'application');
      }

      this.modals.reject.show = false;
      this.modals.reject.targetId = null;
    },

    // User Operations
    suspendUser(id) {
      const userObj = this.users.find(u => u.id === id);
      if (userObj) {
        userObj.status = 'Suspended';
        this.triggerToast(`User "${userObj.name}" has been suspended. System access restricted.`, 'warning');
        this.logActivity(`Administrative suspension assigned to user ${userObj.email}`, 'user');
      }
    },

    activateUser(id) {
      const userObj = this.users.find(u => u.id === id);
      if (userObj) {
        userObj.status = 'Active';
        this.triggerToast(`Suspension revoked for "${userObj.name}". Account reactivated.`, 'success');
        this.logActivity(`Suspension revoked from user account ${userObj.email}`, 'user');
      }
    },

    demoteUser(id) {
      const userObj = this.users.find(u => u.id === id);
      if (userObj) {
        userObj.role = 'Attendee';
        this.triggerToast(`Demoted user "${userObj.name}" to standard attendee role.`, 'warning');
        this.logActivity(`Demoted user ${userObj.email} to Attendee role`, 'user');
      }
    },

    promoteUser(id) {
      const userObj = this.users.find(u => u.id === id);
      if (userObj) {
        userObj.role = 'Organizer';
        this.triggerToast(`Promoted user "${userObj.name}" to platform organizer role.`, 'success');
        this.logActivity(`Promoted user ${userObj.email} to Organizer privileges`, 'user');
      }
    },

    resetUserPassword(id) {
      const userObj = this.users.find(u => u.id === id);
      if (userObj) {
        this.triggerToast(`Temporary password reset credentials dispatched securely to ${userObj.email}.`, 'success');
        this.logActivity(`Dispatched secure manual password reset token for ${userObj.name}`, 'system');
      }
    },

    // Events Operations
    disableEvent(id) {
      const ev = this.events.find(e => e.id === id);
      if (ev) {
        ev.status = 'Disabled';
        this.triggerToast(`Event "${ev.title}" disabled. Public page visibility revoked.`, 'warning');
        this.logActivity(`Disabled event registrations for "${ev.title}" due to administrative block`, 'system');
      }
    },

    enableEvent(id) {
      const ev = this.events.find(e => e.id === id);
      if (ev) {
        ev.status = 'Active';
        this.triggerToast(`Event "${ev.title}" was restored and is now active.`, 'success');
        this.logActivity(`Re-enabled public attendance pathways for "${ev.title}"`, 'system');
      }
    },

    forceCloseRegistration(id) {
      const ev = this.events.find(e => e.id === id);
      if (ev) {
        ev.status = 'Registration Closed';
        this.triggerToast(`Registrations forced closed for "${ev.title}".`, 'warning');
        this.logActivity(`Locked attendee rosters for "${ev.title}"`, 'system');
      }
    },

    openEditEventModal(id) {
      const ev = this.events.find(e => e.id === id);
      if (ev) {
        this.modals.editEvent.targetId = id;
        this.modals.editEvent.title = ev.title;
        this.modals.editEvent.date = ev.date;
        this.modals.editEvent.status = ev.status;
        this.modals.editEvent.organizer = ev.organizer;
        this.modals.editEvent.attendeesCount = ev.attendeesCount;
        this.modals.editEvent.show = true;
      }
    },

    saveEventChanges() {
      const id = this.modals.editEvent.targetId;
      const ev = this.events.find(e => e.id === id);
      if (ev) {
        ev.title = this.modals.editEvent.title;
        ev.date = this.modals.editEvent.date;
        ev.status = this.modals.editEvent.status;
        this.triggerToast(`Successfully updated details for "${ev.title}".`, 'success');
        this.logActivity(`Updated event credentials for "${ev.title}" via Admin Panel`, 'system');
      }
      this.modals.editEvent.show = false;
    },

    // Interactive Attendees listings searcher
    openAttendeesModal(id) {
      this.modals.attendees.targetEventId = id;
      this.modals.attendees.query = '';
      this.modals.attendees.show = true;
    },

    get eventAttendeesList() {
      const ev = this.events.find(e => e.id === this.modals.attendees.targetEventId);
      if (!ev) return [];
      
      const seedAttendees = [
        { name: 'John Doe', email: 'johndoe@gmail.com', ticketType: 'VIP Core Pass', checkedIn: true, time: '14 Mins ago' },
        { name: 'Marcus Aurelius', email: 'philosopher@rome.edu', ticketType: 'General Admission', checkedIn: true, time: '2 Mins ago' },
        { name: 'Livia Drusilla', email: 'livia@empire.gov', ticketType: 'General Admission', checkedIn: false, time: '-' },
        { name: 'Jane Watson', email: 'watson@baker.co.uk', ticketType: 'VIP Access Plus', checkedIn: true, time: '2 Hours ago' },
        { name: 'Alexander G.', email: 'alex@macedonia.world', ticketType: 'Conqueror Pass', checkedIn: false, time: '-' },
        { name: 'Bruce Wayne', email: 'bruce@gothamcorp.com', ticketType: 'VIP Sponsor Tier', checkedIn: false, time: '-' }
      ];

      const q = this.modals.attendees.query.toLowerCase().trim();
      if (!q) return seedAttendees;
      return seedAttendees.filter(a => a.name.toLowerCase().includes(q) || a.email.toLowerCase().includes(q) || a.ticketType.toLowerCase().includes(q));
    },

    // Assign / Remove event Validators
    openAssignValidatorModal(id) {
      this.modals.assignValidator.targetId = id;
      this.modals.assignValidator.selectedEvent = '';
      this.modals.assignValidator.show = true;
    },

    assignValidator() {
      const vId = this.modals.assignValidator.targetId;
      const targetEventTitle = this.modals.assignValidator.selectedEvent;
      
      if (!targetEventTitle) {
        this.triggerToast('You must select a valid event to assign to.', 'error');
        return;
      }
      
      const val = this.validators.find(v => v.id === vId);
      if (val) {
        if (val.assignedEvents.includes(targetEventTitle)) {
          this.triggerToast(`Validator is already assigned to "${targetEventTitle}".`, 'info');
          return;
        }
        val.assignedEvents.push(targetEventTitle);
        val.status = 'Active';
        this.triggerToast(`Assigned ${val.name} to validator pool for "${targetEventTitle}"`, 'success');
        this.logActivity(`Assigned validator ${val.name} to oversee tickets for "${targetEventTitle}"`, 'system');
      }
      this.modals.assignValidator.show = false;
    },

    removeValidatorEvent(valId, eventTitle) {
      const val = this.validators.find(v => v.id === valId);
      if (val) {
        val.assignedEvents = val.assignedEvents.filter(e => e !== eventTitle);
        if (val.assignedEvents.length === 0) {
          val.status = 'Inactive';
        }
        this.triggerToast(`Removed validator role for ${val.name} from "${eventTitle}".`, 'info');
        this.logActivity(`Revoked ${val.name}'s scanner privileges for "${eventTitle}"`, 'system');
      }
    },

    // Filters computed lists
    get filteredApplications() {
      const q = this.searchQueries.applications.toLowerCase();
      return this.applications.filter(app => {
        const matchesSearch = app.userName.toLowerCase().includes(q) || 
                              app.orgName.toLowerCase().includes(q) || 
                              app.email.toLowerCase().includes(q) ||
                              app.country.toLowerCase().includes(q);
        
        const matchesFilter = this.filters.applications === 'all' || app.status === this.filters.applications;
        return matchesSearch && matchesFilter;
      });
    },

    get filteredUsers() {
      const q = this.searchQueries.users.toLowerCase();
      return this.users.filter(u => {
        const matchesSearch = u.name.toLowerCase().includes(q) || 
                              u.email.toLowerCase().includes(q);
                              
        let matchesFilter = true;
        if (this.filters.users !== 'all') {
          if (this.filters.users === 'Suspended') {
            matchesFilter = u.status === 'Suspended';
          } else {
            matchesFilter = u.role === this.filters.users;
          }
        }
        return matchesSearch && matchesFilter;
      });
    },

    get filteredEvents() {
      const q = this.searchQueries.events.toLowerCase();
      return this.events.filter(e => {
        const matchesSearch = e.title.toLowerCase().includes(q) || 
                              e.organizer.toLowerCase().includes(q);
                              
        const matchesFilter = this.filters.events === 'all' || e.status === this.filters.events;
        return matchesSearch && matchesFilter;
      });
    },

    get filteredValidators() {
      const q = this.searchQueries.validators.toLowerCase();
      return this.validators.filter(v => {
        return v.name.toLowerCase().includes(q) || v.email.toLowerCase().includes(q);
      });
    }
  }));
});
