
"use strict";

const translations = {
  gu: {
    navBook: "બુકિંગ",
    navServices: "સેવાઓ",
    navAbout: "અમારા વિશે",
    login: "લોગિન",
    eyebrow: "ભારતનું Mobility Platform",
    heroTitle: "દરેક મુસાફરી માટે વિશ્વાસપાત્ર સાથી.",
    heroDescription: "Bike, Auto અને Car ની રાઇડ એક જ પ્લેટફોર્મ પરથી સરળતાથી શોધો અને બુક કરો.",
    startBooking: "રાઇડ બુક કરો",
    madeIndia: "ભારત માટે બનાવેલું",
    travel: "તમારી મુસાફરી",
    travelSmart: "સ્માર્ટ મુસાફરી",
    bookingLabel: "રાઇડ બુક કરો",
    bookingTitle: "તમારી મુસાફરી શરૂ કરો",
    bookingDescription: "Pickup, Destination અને તમારું વાહન પસંદ કરો.",
    pickup: "Pickup Location",
    destination: "Destination",
    vehicleTitle: "વાહન પસંદ કરો",
    vehicleSubtitle: "તમારી જરૂરિયાત મુજબ",
    selectedVehicle: "પસંદ કરેલું વાહન",
    findRide: "રાઇડ શોધો",
    disclaimer: "ભાડું, વાહનની ઉપલબ્ધતા અને બુકિંગની પુષ્ટિ Backend સાથે જોડાયા પછી મળશે.",
    bikeDesc: "ઝડપી મુસાફરી",
    autoDesc: "રોજિંદી મુસાફરી",
    economyDesc: "કિફાયતી કાર",
    premiumDesc: "આરામદાયક મુસાફરી",
    servicesLabel: "અમારી સેવાઓ",
    servicesTitle: "એક પ્લેટફોર્મ, અનેક મુસાફરી વિકલ્પો",
    bikeText: "ઝડપી અને સરળ શહેરી મુસાફરી.",
    autoText: "રોજિંદી મુસાફરી માટે અનુકૂળ.",
    carText: "વ્યક્તિગત અને આરામદાયક મુસાફરી.",
    portalLabel: "પ્લેટફોર્મ પ્રવેશ",
    portalTitle: "તમારા માટે યોગ્ય Portal પસંદ કરો",
    passengerDesc: "રાઇડ બુક કરો અને તમારી મુસાફરીનું સંચાલન કરો.",
    driverDesc: "રાઇડ રિક્વેસ્ટ, ટ્રિપ અને કમાણીનું સંચાલન કરો.",
    adminDesc: "પ્લેટફોર્મ, યુઝર્સ અને બુકિંગનું નિયંત્રણ કરો.",
    footerText: "ભારત માટે આધુનિક Mobility Platform."
  },

  en: {
    navBook: "Booking",
    navServices: "Services",
    navAbout: "About",
    login: "Login",
    eyebrow: "INDIA'S MOBILITY PLATFORM",
    heroTitle: "A trusted partner for every journey.",
    heroDescription: "Discover and book Bike, Auto and Car rides from one platform.",
    startBooking: "Book a Ride",
    madeIndia: "Made for India",
    travel: "Your Journey",
    travelSmart: "Travel Smarter",
    bookingLabel: "BOOK YOUR RIDE",
    bookingTitle: "Start Your Journey",
    bookingDescription: "Choose your pickup, destination and vehicle.",
    pickup: "Pickup Location",
    destination: "Destination",
    vehicleTitle: "Select Your Vehicle",
    vehicleSubtitle: "Choose what suits your journey",
    selectedVehicle: "Selected Vehicle",
    findRide: "Find a Ride",
    disclaimer: "Fare, vehicle availability and booking confirmation will be provided after Backend integration.",
    bikeDesc: "Quick Rides",
    autoDesc: "Everyday Travel",
    economyDesc: "Affordable Cars",
    premiumDesc: "Premium Comfort",
    servicesLabel: "OUR SERVICES",
    servicesTitle: "One Platform, Multiple Ride Options",
    bikeText: "Fast and convenient city travel.",
    autoText: "Convenient everyday transportation.",
    carText: "Comfortable personal transportation.",
    portalLabel: "PLATFORM ACCESS",
    portalTitle: "Choose Your Portal",
    passengerDesc: "Book rides and manage your journeys.",
    driverDesc: "Manage ride requests, trips and earnings.",
    adminDesc: "Manage the platform, users and bookings.",
    footerText: "A modern mobility platform for India."
  }
};

const languageSelect = document.getElementById("language");
const themeButton = document.getElementById("themeBtn");

function setLanguage(language) {
  const words = translations[language];

  if (!words) return;

  document.documentElement.lang = language;

  document.querySelectorAll("[data-i18n]").forEach(element => {
    const key = element.dataset.i18n;

    if (words[key]) {
      element.textContent = words[key];
    }
  });

  languageSelect.value = language;

  try {
    localStorage.setItem("indianTaxiLanguage", language);
  } catch (error) {
    console.warn("Language preference unavailable.");
  }
}

function setTheme(theme) {
  const dark = theme === "dark";

  document.body.classList.toggle("dark", dark);
  themeButton.textContent = dark ? "☀" : "☾";

  try {
    localStorage.setItem("indianTaxiTheme", theme);
  } catch (error) {
    console.warn("Theme preference unavailable.");
  }
}

languageSelect.addEventListener("change", event => {
  setLanguage(event.target.value);
});

themeButton.addEventListener("click", () => {
  const current = document.body.classList.contains("dark");
  setTheme(current ? "light" : "dark");
});

let selectedVehicle = "bike";

const vehicleNames = {
  bike: "Bike",
  auto: "Auto",
  economy: "Economy",
  premium: "Premium"
};

document.querySelectorAll(".vehicle-card").forEach(card => {
  card.addEventListener("click", () => {

    document.querySelectorAll(".vehicle-card").forEach(item => {
      item.classList.remove("selected");
    });

    card.classList.add("selected");

    selectedVehicle = card.dataset.type;

    document.getElementById("selectedVehicle").textContent =
      vehicleNames[selectedVehicle];
  });
});

document.getElementById("findRide").addEventListener("click", () => {

  const pickup = document.getElementById("pickup").value.trim();
  const destination = document.getElementById("destination").value.trim();

  const message = document.getElementById("bookingMessage");

  if (!pickup || !destination) {
    message.textContent =
      "Please enter both Pickup and Destination.";
    return;
  }

  if (pickup.toLowerCase() === destination.toLowerCase()) {
    message.textContent =
      "Pickup and Destination must be different.";
    return;
  }

  message.textContent =
    "Your ride details are ready. Booking API integration is the next development step.";

});

try {
  const savedLanguage = localStorage.getItem("indianTaxiLanguage");
  const savedTheme = localStorage.getItem("indianTaxiTheme");

  setLanguage(translations[savedLanguage] ? savedLanguage : "gu");

  if (savedTheme === "dark" || savedTheme === "light") {
    setTheme(savedTheme);
  } else {
    setTheme("light");
  }

} catch (error) {
  setLanguage("gu");
  setTheme("light");
}
