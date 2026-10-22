
(() => {
    "use strict";

    const panel = document.getElementById("cafe-assistant");
    const toggle = document.getElementById("cafe-assistant-toggle");

    if (!panel || !toggle) return;

    const form = panel.querySelector("#cafe-assistant-form");
    const input = panel.querySelector("#cafe-assistant-input");
    const messages = panel.querySelector("#cafe-assistant-messages");
    const closeButton = panel.querySelector("#cafe-assistant-close");

    if (!form || !input || !messages || !closeButton) return;

    const answers = [
        {
            keywords: ["hello", "hey", "help"],
            answer: "Hello! Welcome to CaféQuick. I can help with menus, ordering, carts and demo payments. What would you like to know?"
        },
        {
            keywords: ["menu", "drink", "coffee", "tea", "price", "cafe", "café"],
            answer: "You can browse our six cafés and open View Menu to see available drinks and prices. Choose a quantity, then select Add to Cart."
        },
        {
            keywords: ["cart", "basket", "add"],
            answer: "Open a café's menu, choose a quantity for a drink and select Add to Cart. Use View Cart to review your selections and totals."
        },
        {
            keywords: ["checkout", "pay", "payment", "money"],
            answer: "CaféQuick currently uses a simulated demo payment. It does not take real money. Sign in and follow the checkout steps to try the demo."
        },
        {
            keywords: ["order status", "track order", "where is my order", "order history"],
            answer: "You can view your orders in Order History after signing in. I can't look up a specific order from this chat yet."
        },
        {
            keywords: ["pickup", "collect", "collection", "pickup time"],
            answer: "Please check the information shown by CaféQuick for your order. This assistant cannot confirm or change a pickup time yet."
        },
        {
            keywords: ["cancel", "cancellation"],
            answer: "I can't cancel orders from this chat yet. Please check the order information or contact the café directly before assuming an order has been cancelled."
        },
        {
            keywords: ["blind", "screen reader", "accessibility", "keyboard"],
            answer: "We're working to make CaféQuick easier to use with keyboards and screen readers. You can navigate this chat with Tab, Shift+Tab and Enter."
        }
    ];

    function addMessage(text, sender) {
        const message = document.createElement("p");
        message.className = `cafe-assistant-message ${sender}`;
        message.textContent = text;
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
    }

    function findAnswer(question) {
        const normalized = question.toLocaleLowerCase().trim();
        const words = normalized.match(/[\p{L}\p{N}']+/gu) || [];

        const match = answers.find(entry =>
            entry.keywords.some(keyword => {
                if (keyword.includes(" ")) {
                    return normalized.includes(keyword);
                }

                return words.includes(keyword);
            })
        );

        return match
            ? match.answer
            : "I'm still learning. Try asking about café menus, adding items to your cart, demo payments, order history or accessibility.";
    }

    function openAssistant() {
        panel.hidden = false;
        toggle.setAttribute("aria-expanded", "true");
        input.focus();
    }

    function closeAssistant() {
        panel.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
    }

    toggle.addEventListener("click", () => {
        if (panel.hidden) {
            openAssistant();
        } else {
            closeAssistant();
        }
    });

    closeButton.addEventListener("click", closeAssistant);

    form.addEventListener("submit", event => {
        event.preventDefault();

        const question = input.value.trim();
        if (!question) {
            input.focus();
            return;
        }

        addMessage(`You asked: ${question}`, "user");
        addMessage(findAnswer(question), "assistant");

        input.value = "";
        input.focus();
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && !panel.hidden) {
            closeAssistant();
        }
    });
})();