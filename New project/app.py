import re
from urllib.parse import quote_plus
import streamlit as st
PRODUCTS = []
CATEGORIES = [
    "Processor",
    "Motherboard",
    "RAM",
    "ROM / Storage",
    "Graphics Card",
    "Wi-Fi Card",
    "Power Supply",
    "Cabinet",
]
def rupees(amount):
    return f"₹{amount:,.0f}"
def price_of(product):
    return product["price"]
def price_range(product):
    low = product.get("price_low", round(product["price"] * 0.88))
    high = product.get("price_high", round(product["price"] * 1.15))
    if product["price"] == 0:
        return "Included / not needed"
    return f"{rupees(low)} - {rupees(high)}"
def products_in(category):
    return [product for product in PRODUCTS if product["category"] == category]
def image_url_for(part):
    search_words = {
        "Processor": "amd processor chip",
        "Motherboard": "computer motherboard",
        "RAM": "computer ram memory",
        "ROM / Storage": "nvme ssd storage",
        "Graphics Card": "amd radeon graphics card",
        "Wi-Fi Card": "pcie wifi card",
        "Power Supply": "computer power supply",
        "Cabinet": "computer pc case",
    }
    query = quote_plus(search_words.get(part["category"], part["name"]))
    return f"https://source.unsplash.com/700x420/?{query}"
def search_link(site, product_name):
    query = quote_plus(product_name)
    links = {
        "Amazon India": f"https://www.amazon.in/s?k={query}",
        "MDComputers": f"https://mdcomputers.in/index.php?route=product/search&search={query}",
        "PrimeABGB": f"https://www.primeabgb.com/?s={query}&post_type=product",
        "Photos": f"https://www.google.com/search?tbm=isch&q={query}",
    }
    return links[site]
def apply_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                linear-gradient(135deg, rgba(247, 250, 252, 0.94), rgba(235, 244, 241, 0.96)),
                radial-gradient(circle at top left, rgba(15, 139, 141, 0.14), transparent 34%),
                radial-gradient(circle at bottom right, rgba(199, 144, 37, 0.12), transparent 32%);
            color: #17202a;
        }
        .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
        .stMarkdown, .stMarkdown p, .stCaptionContainer,
        [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p,
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
        [data-testid="stMarkdownContainer"],
        [data-testid="stExpander"] {
            color: #111111 !important;
        }
        input, textarea, select {
            color: #111111 !important;
        }
        .block-container {
            max-width: 1220px;
            padding-top: 1.4rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3 {
            letter-spacing: 0;
        }
        h1 {
            font-size: 3.3rem !important;
            line-height: 1.02 !important;
            margin-bottom: 0.4rem !important;
        }
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #d7dde3;
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 10px 30px rgba(23, 32, 42, 0.08);
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #d7dde3 !important;
            border-radius: 8px !important;
            box-shadow: 0 12px 32px rgba(23, 32, 42, 0.08);
            background: rgba(255, 255, 255, 0.92);
        }
        div.stButton > button {
            background: #0f8b8d;
            color: white;
            border: 0;
            border-radius: 8px;
            min-height: 3rem;
            font-weight: 800;
        }
        div.stButton > button:hover {
            background: #0b6769;
            color: white;
            border: 0;
        }
        div[data-testid="stLinkButton"] a {
            border-radius: 8px;
            border: 1px solid #0f8b8d;
            color: #0b6769;
            font-weight: 700;
        }
        .hero-copy {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid #d7dde3;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 20px 50px rgba(23, 32, 42, 0.1);
        }
        .hero-kicker {
            color: #0b6769;
            font-weight: 900;
            text-transform: uppercase;
            font-size: 0.78rem;
        }
        .hero-subtext {
            color: #111111;
            font-size: 1.05rem;
            line-height: 1.6;
        }
        img {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
PRODUCTS.extend(
    [
        # AMD and Snapdragon processors only. Snapdragon is treated as an
        # integrated mini-PC platform because it is not a normal socketed CPU.
        {
            "category": "Processor",
            "name": "AMD Ryzen 5 5600",
            "brand": "AMD",
            "price": 12100,
            "office": 82,
            "gaming": 76,
            "home": 80,
            "creator": 72,
            "socket": "AM4",
            "wattage": 65,
            "capability": 72,
            "details": "6 cores, 12 threads, DDR4 value build",
        },
        {
            "category": "Processor",
            "name": "AMD Ryzen 5 7600",
            "brand": "AMD",
            "price": 18900,
            "office": 88,
            "gaming": 88,
            "home": 86,
            "creator": 82,
            "socket": "AM5",
            "wattage": 65,
            "capability": 84,
            "details": "6 cores, 12 threads, DDR5 platform",
        },
        {
            "category": "Processor",
            "name": "AMD Ryzen 7 7700",
            "brand": "AMD",
            "price": 28600,
            "office": 92,
            "gaming": 91,
            "home": 88,
            "creator": 90,
            "socket": "AM5",
            "wattage": 65,
            "capability": 90,
            "details": "8 cores, efficient gaming/editing CPU",
        },
        {
            "category": "Processor",
            "name": "AMD Ryzen 7 7800X3D",
            "brand": "AMD",
            "price": 36500,
            "office": 90,
            "gaming": 98,
            "home": 88,
            "creator": 86,
            "socket": "AM5",
            "wattage": 120,
            "capability": 95,
            "details": "Excellent gaming CPU with 3D V-Cache",
        },
        {
            "category": "Processor",
            "name": "AMD Ryzen 9 7900",
            "brand": "AMD",
            "price": 39800,
            "office": 96,
            "gaming": 92,
            "home": 90,
            "creator": 96,
            "socket": "AM5",
            "wattage": 65,
            "capability": 96,
            "details": "12 cores, strong for editing and multitasking",
        },
        {
            "category": "Processor",
            "name": "Snapdragon X Elite Mini PC Platform",
            "brand": "Snapdragon",
            "price": 42000,
            "office": 94,
            "gaming": 38,
            "home": 88,
            "creator": 68,
            "socket": "SNAPDRAGON-X",
            "wattage": 35,
            "capability": 76,
            "details": "Efficient ARM platform, best for office/home",
        },
        {
            "category": "Motherboard",
            "name": "B550M AM4 DDR4 Motherboard",
            "price": 8800,
            "office": 80,
            "gaming": 78,
            "home": 76,
            "creator": 76,
            "socket": "AM4",
            "ram_type": "DDR4",
            "size": "mATX",
            "tier": "budget",
            "details": "AM4, DDR4, mATX, good budget choice",
        },
        {
            "category": "Motherboard",
            "name": "A620M AM5 DDR5 Motherboard",
            "price": 9700,
            "office": 82,
            "gaming": 76,
            "home": 80,
            "creator": 76,
            "socket": "AM5",
            "ram_type": "DDR5",
            "size": "mATX",
            "tier": "budget",
            "details": "AM5, DDR5, cheaper motherboard spend",
        },
        {
            "category": "Motherboard",
            "name": "B650M AM5 DDR5 Motherboard",
            "price": 13700,
            "office": 88,
            "gaming": 88,
            "home": 84,
            "creator": 86,
            "socket": "AM5",
            "ram_type": "DDR5",
            "size": "mATX",
            "tier": "balanced",
            "details": "AM5, DDR5, balanced upgrade path",
        },
        {
            "category": "Motherboard",
            "name": "X670E AM5 DDR5 Motherboard",
            "price": 29500,
            "office": 92,
            "gaming": 94,
            "home": 86,
            "creator": 96,
            "socket": "AM5",
            "ram_type": "DDR5",
            "size": "ATX",
            "tier": "premium",
            "details": "AM5, DDR5, high-end expansion",
        },
        {
            "category": "Motherboard",
            "name": "Snapdragon X Integrated Board",
            "price": 0,
            "office": 90,
            "gaming": 35,
            "home": 86,
            "creator": 64,
            "socket": "SNAPDRAGON-X",
            "ram_type": "LPDDR5X",
            "size": "Mini",
            "tier": "integrated",
            "details": "Integrated board for Snapdragon builds",
        },
    ]
)
def guess_use_cases(user_text):
    text = user_text.lower()
    use_cases = []
    if re.search("office|excel|coding|work|business|study", text):
        use_cases.append("office")
    if re.search("game|gaming|edit|editing|render|stream|youtube|premiere", text):
        use_cases.append("gaming")
        use_cases.append("creator")
    if re.search("home|movie|browsing|school|family|daily", text):
        use_cases.append("home")
    return use_cases
def guess_budget(user_text):
    text = user_text.lower().replace(",", "")
    lakh_match = re.search(r"(\d+(?:\.\d+)?)\s*(lakh|lac|l)", text)
    if lakh_match:
        return clean_budget(float(lakh_match.group(1)) * 100000)
    thousand_match = re.search(r"(\d+(?:\.\d+)?)\s*(k|thousand)", text)
    if thousand_match:
        return clean_budget(float(thousand_match.group(1)) * 1000)
    rupee_match = re.search(r"(?:rs\.?|inr)?\s*(\d{5,6})", text)
    if rupee_match:
        return clean_budget(float(rupee_match.group(1)))
    return None
def guess_budget_range(user_text):
    text = user_text.lower().replace(",", "")
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*(lakh|lac|l|k|thousand)?", text)
    values = []
    for number, unit in matches:
        value = float(number)
        if unit in ["lakh", "lac", "l"]:
            value = value * 100000
        elif unit in ["k", "thousand"]:
            value = value * 1000
        elif value < 1000:
            continue
        if value >= 25000:
            values.append(clean_budget(value))
    if len(values) >= 2:
        low = min(values[0], values[1])
        high = max(values[0], values[1])
        return low, high
    if len(values) == 1:
        budget = values[0]
        return clean_budget(budget * 0.90), clean_budget(budget * 1.10)
    return None
def clean_budget(amount):
    rounded = round(amount / 5000) * 5000
    return int(max(25000, min(250000, rounded)))
def product_score(product, use_cases):
    return sum(product[use_case] for use_case in use_cases) / len(use_cases)
def fuzzy_ratio(value, target):
    ratio = value / target
    if ratio >= 1:
        return min(1.25, ratio)
    return ratio
def needed_processor_capability(use_cases, budget, cpu_priority):
    target = 60
    if "gaming" in use_cases:
        target = max(target, 84)
    if "creator" in use_cases:
        target = max(target, 90)
    if "office" in use_cases:
        target = max(target, 68)
    if budget > 200000:
        target = max(target, 94)
    if cpu_priority == "Strong processor":
        target = target + 8
    if cpu_priority == "Save money on processor":
        target = target - 8
    return min(100, max(45, target))
def processor_fuzzy_score(processor, use_cases, budget, cpu_priority):
    target = needed_processor_capability(use_cases, budget, cpu_priority)
    capability_fit = fuzzy_ratio(processor["capability"], target) * 100
    task_fit = product_score(processor, use_cases)
    price_penalty = price_of(processor) / max(1, budget) * 45
    return capability_fit * 0.55 + task_fit * 0.45 - price_penalty
def gpu_fuzzy_score(graphics_card, use_cases, budget, gpu_need):
    if gpu_need == "No dedicated GPU needed":
        target_speed = 20
    elif "creator" in use_cases:
        target_speed = 88
    elif "gaming" in use_cases:
        target_speed = 82
    else:
        target_speed = 35

    if budget > 200000 and gpu_need != "No dedicated GPU needed":
        target_speed = max(target_speed, 94)

    speed_fit = fuzzy_ratio(graphics_card["speed"], target_speed) * 100
    task_fit = product_score(graphics_card, use_cases)
    price_penalty = price_of(graphics_card) / max(1, budget) * 35
    return speed_fit * 0.6 + task_fit * 0.4 - price_penalty
def product_allowed(product, preferences, budget):
    category = product["category"]
    if category == "RAM":
        allowed_sizes = [32] if budget > 200000 else preferences["ram_sizes"]
        if product["gb"] not in allowed_sizes:
            return False
        if preferences["ram_type"] != "Any" and product["ram_type"] != preferences["ram_type"]:
            return False
    if category == "ROM / Storage":
        allowed_storage = preferences["storage_sizes"]
        if budget > 200000:
            allowed_storage = [size for size in allowed_storage if size >= 1024]
        if product["storage_gb"] not in allowed_storage:
            return False
    if category == "Graphics Card":
        if preferences["gpu_need"] == "No dedicated GPU needed":
            return price_of(product) == 0
        return product["brand"] == "AMD"

    if category == "Wi-Fi Card" and not preferences["include_wifi"]:
        return False

    return True
def is_compatible(processor, motherboard, ram, graphics_card, wifi_card, power_supply, cabinet):
    if processor["socket"] != motherboard["socket"]:
        return False
    if ram["ram_type"] != motherboard["ram_type"]:
        return False
    if motherboard["size"] not in cabinet["supported_sizes"]:
        return False
    if processor["socket"] == "SNAPDRAGON-X" and wifi_card is not None:
        return False

    estimated_watts = processor["wattage"] + graphics_card["wattage"] + 110
    return power_supply["capacity"] >= estimated_watts * 1.35
def find_part(parts, category):
    for part in parts:
        if part["category"] == category:
            return part
    return None
def calculate_build_score(parts, use_cases, total_price, min_budget, max_budget, preferences):
    target_budget = (min_budget + max_budget) / 2
    processor = find_part(parts, "Processor")
    graphics_card = find_part(parts, "Graphics Card")
    motherboard = find_part(parts, "Motherboard")
    ram = find_part(parts, "RAM")
    storage = find_part(parts, "ROM / Storage")
    power_supply = find_part(parts, "Power Supply")
    cabinet = find_part(parts, "Cabinet")
    wifi_card = find_part(parts, "Wi-Fi Card")

    score = sum(product_score(part, use_cases) for part in parts)
    score = score + processor_fuzzy_score(
        processor,
        use_cases,
        target_budget,
        preferences["cpu_priority"],
    ) * 1.4
    score = score + gpu_fuzzy_score(graphics_card, use_cases, target_budget, preferences["gpu_need"]) * 1.2
    score = score + 100 - abs(target_budget - total_price) / 1000

    if preferences["motherboard_spend"] == "Save money on motherboard":
        if motherboard["tier"] == "budget":
            score = score + 35
        if motherboard["tier"] == "premium":
            score = score - 35

    if preferences["psu_quality"]:
        score = score + power_supply["quality"] * 0.35
    if preferences["case_quality"]:
        score = score + cabinet["airflow"] * 0.35
    if preferences["ram_priority"]:
        score = score + ram["gb"] * 2
    if preferences["less_storage"]:
        score = score - price_of(storage) / 400
    if wifi_card is not None:
        score = score + wifi_card["wifi_rank"] * 0.25

    return score
def find_best_pc(use_cases, min_budget, max_budget, preferences):
    target_budget = (min_budget + max_budget) / 2
    best_build = None
    best_score = -10**9
    processors = products_in("Processor")
    processors.sort(
        key=lambda processor: processor_fuzzy_score(
            processor,
            use_cases,
            target_budget,
            preferences["cpu_priority"],
        ),
        reverse=True,
    )
    # Processor is ranked first, then the other categories are tested.
    for processor in processors:
        for motherboard in products_in("Motherboard"):
            for ram in products_in("RAM"):
                if not product_allowed(ram, preferences, max_budget):
                    continue
                for storage in products_in("ROM / Storage"):
                    if not product_allowed(storage, preferences, max_budget):
                        continue
                    for graphics_card in products_in("Graphics Card"):
                        if not product_allowed(graphics_card, preferences, max_budget):
                            continue
                        wifi_options = products_in("Wi-Fi Card") if preferences["include_wifi"] else [None]
                        for wifi_card in wifi_options:
                            for power_supply in products_in("Power Supply"):
                                for cabinet in products_in("Cabinet"):
                                    if not is_compatible(
                                        processor,
                                        motherboard,
                                        ram,
                                        graphics_card,
                                        wifi_card,
                                        power_supply,
                                        cabinet,
                                    ):
                                        continue

                                    parts = [
                                        processor,
                                        motherboard,
                                        ram,
                                        storage,
                                        graphics_card,
                                        power_supply,
                                        cabinet,
                                    ]
                                    if wifi_card is not None:
                                        parts.append(wifi_card)

                                    total_price = sum(price_of(part) for part in parts)
                                    if total_price > max_budget:
                                        continue

                                    score = calculate_build_score(
                                        parts,
                                        use_cases,
                                        total_price,
                                        min_budget,
                                        max_budget,
                                        preferences,
                                    )

                                    if total_price < min_budget:
                                        score = score - 20

                                    if score > best_score:
                                        best_score = score
                                        best_build = {"parts": parts, "total_price": total_price}

    if best_build is None:
        best_build = find_cheapest_pc(preferences, max_budget)

    best_build["alternatives"] = find_alternatives(best_build, use_cases, max_budget, preferences)
    return best_build
def find_cheapest_pc(preferences, budget):
    backup_preferences = preferences.copy()
    backup_preferences["gpu_need"] = "No dedicated GPU needed"
    backup_preferences["include_wifi"] = False
    cheapest = None
    cheapest_price = 10**9

    for processor in products_in("Processor"):
        for motherboard in products_in("Motherboard"):
            for ram in products_in("RAM"):
                if not product_allowed(ram, backup_preferences, budget):
                    continue
                for storage in products_in("ROM / Storage"):
                    if not product_allowed(storage, backup_preferences, budget):
                        continue
                    for graphics_card in products_in("Graphics Card"):
                        if not product_allowed(graphics_card, backup_preferences, budget):
                            continue
                        for power_supply in products_in("Power Supply"):
                            for cabinet in products_in("Cabinet"):
                                if not is_compatible(
                                    processor,
                                    motherboard,
                                    ram,
                                    graphics_card,
                                    None,
                                    power_supply,
                                    cabinet,
                                ):
                                    continue
                                parts = [
                                    processor,
                                    motherboard,
                                    ram,
                                    storage,
                                    graphics_card,
                                    power_supply,
                                    cabinet,
                                ]
                                total_price = sum(price_of(part) for part in parts)
                                if total_price < cheapest_price:
                                    cheapest_price = total_price
                                    cheapest = {"parts": parts, "total_price": total_price}

    return cheapest
def replace_part(parts, category, new_part):
    return [new_part if part["category"] == category else part for part in parts]
def test_build_is_compatible(parts):
    return is_compatible(
        find_part(parts, "Processor"),
        find_part(parts, "Motherboard"),
        find_part(parts, "RAM"),
        find_part(parts, "Graphics Card"),
        find_part(parts, "Wi-Fi Card"),
        find_part(parts, "Power Supply"),
        find_part(parts, "Cabinet"),
    )
def find_alternatives(build, use_cases, budget, preferences):
    alternatives = {}

    for category in CATEGORIES:
        selected_part = find_part(build["parts"], category)
        if selected_part is None:
            continue

        price_without_selected = build["total_price"] - price_of(selected_part)
        options = []

        for option in products_in(category):
            if option["name"] == selected_part["name"]:
                continue
            if not product_allowed(option, preferences, budget):
                continue
            if price_without_selected + price_of(option) > budget * 1.18:
                continue
            test_parts = replace_part(build["parts"], category, option)
            if not test_build_is_compatible(test_parts):
                continue
            options.append(option)

        options.sort(
            key=lambda product: product_score(product, use_cases) / max(1, price_of(product)),
            reverse=True,
        )
        alternatives[category] = options[:2]

    return alternatives


def show_part_card(part, alternatives):
    with st.container(border=True):
        st.subheader(part["category"])
        st.image(image_url_for(part), caption=f"{part['category']} reference photo")
        st.write(f"**{part['name']}**")
        st.write(f"Estimated price range: {price_range(part)}")
        st.caption(part["details"])

        if part["category"] == "Processor":
            st.progress(part["capability"] / 100, text=f"Processor capability: {part['capability']}/100")
        if part["category"] == "Graphics Card":
            st.progress(part["speed"] / 100, text=f"GPU speed/capability: {part['speed']}/100")

        if alternatives:
            st.write("Alternative options:")
            for option in alternatives:
                st.write(f"- {option['name']} - {price_range(option)}")
        else:
            st.write("No close alternative in this budget.")

        link_col1, link_col2, link_col3, link_col4 = st.columns(4)
        with link_col1:
            st.link_button("Amazon", search_link("Amazon India", part["name"]))
        with link_col2:
            st.link_button("MDComputers", search_link("MDComputers", part["name"]))
        with link_col3:
            st.link_button("PrimeABGB", search_link("PrimeABGB", part["name"]))
        with link_col4:
            st.link_button("Photos", search_link("Photos", part["name"]))


def get_preferences(budget):
    st.subheader("Detailed requirements")

    cpu_priority = st.radio(
        "Processor requirement",
        ["Balanced processor", "Strong processor", "Save money on processor"],
        horizontal=True,
    )

    motherboard_spend = st.radio(
        "Motherboard spending",
        ["Balanced motherboard", "Save money on motherboard", "Premium motherboard"],
        horizontal=True,
    )

    if budget > 200000:
        st.info("Budget is above ₹2,00,000, so RAM is locked to 32GB.")
        ram_sizes = [32]
    else:
        ram_sizes = st.multiselect(
            "RAM size allowed",
            [8, 16, 32],
            default=[16, 32],
            format_func=lambda size: f"{size}GB",
        )
        if not ram_sizes:
            ram_sizes = [16]

    ram_type = st.selectbox("RAM generation", ["Any", "DDR5", "DDR4"])

    if budget > 200000:
        st.info("Budget is above ₹2,00,000, so 256GB and 512GB storage are hidden.")
        storage_sizes = [1024, 2048]
    else:
        storage_sizes = st.multiselect(
            "ROM / storage size allowed",
            [256, 512, 1024, 2048],
            default=[512, 1024],
            format_func=lambda size: "1TB" if size == 1024 else "2TB" if size == 2048 else f"{size}GB",
        )
        if not storage_sizes:
            storage_sizes = [512]

    return {
        "cpu_priority": cpu_priority,
        "motherboard_spend": motherboard_spend,
        "ram_sizes": ram_sizes,
        "ram_type": ram_type,
        "storage_sizes": storage_sizes,
        "ram_priority": st.checkbox("I need fire RAM / more memory performance"),
        "less_storage": st.checkbox("Less ROM/storage is okay"),
        "psu_quality": st.checkbox("I want a stronger power supply"),
        "case_quality": st.checkbox("I want a better airflow cabinet"),
        "include_wifi": st.checkbox("Add Wi-Fi card, Wi-Fi 6E or better"),
        "gpu_need": st.radio(
            "Graphics card requirement",
            ["AMD dedicated GPU", "No dedicated GPU needed"],
            horizontal=True,
        ),
    }
def run_app():
    st.set_page_config(page_title="PC Builder India", layout="wide")
    apply_theme()

    hero_text, hero_image = st.columns([1.1, 0.9], vertical_alignment="center")
    with hero_text:
        st.markdown(
            """
            <div class="hero-copy">
              <div class="hero-kicker">PC Builder India</div>
              <h1>Build a sharper PC for your budget.</h1>
              <div class="hero-subtext">
                Pick the job, budget range, RAM, storage, processor priority,
                Wi-Fi, PSU and case needs. The builder checks compatibility and
                gives alternatives with shopping links.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hero_image:
        st.image(
            "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?auto=format&fit=crop&w=1200&q=80",
            caption="Reference setup",
            use_container_width=True,
        )

    st.write("")
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Catalog parts", len(PRODUCTS))
    metric2.metric("GPU policy", "AMD only")
    metric3.metric("Wi-Fi", "6E+")
    with st.expander("Where this data comes from"):
        st.write(
            "The current app uses a starter product database written in Python. "
            "The prices are estimated ranges, not live scraped prices."
        )
        st.write(
            "The product names are based on common AMD Ryzen, Snapdragon, Radeon, "
            "Wi-Fi 6E/Wi-Fi 7, PSU, cabinet, RAM, and SSD categories. "
            "Use the shopping buttons on each part to check the current live price."
        )
        st.write(
            "For a production version, the next step is replacing the PRODUCTS list "
            "with live store APIs or a backend price scraper."
        )

    user_text = st.text_area(
        "What should your PC do?",
        placeholder="Example: I want a gaming and video editing PC around 85000",
    )

    st.write("Choose one or more:")
    wants_office = st.checkbox("Office")
    wants_gaming = st.checkbox("Gaming / Video Editing")
    wants_home = st.checkbox("Home")

    budget_col1, budget_col2 = st.columns(2)
    with budget_col1:
        min_budget = st.number_input(
            "Minimum budget in rupees",
            min_value=25000,
            max_value=250000,
            value=70000,
            step=5000,
        )
    with budget_col2:
        max_budget = st.number_input(
            "Maximum budget in rupees",
            min_value=25000,
            max_value=250000,
            value=90000,
            step=5000,
        )

    guessed_range = guess_budget_range(user_text)
    if guessed_range is not None:
        min_budget, max_budget = guessed_range
        st.info(f"Budget range detected from your text: {rupees(min_budget)} to {rupees(max_budget)}")

    if min_budget > max_budget:
        min_budget, max_budget = max_budget, min_budget
        st.warning("Minimum budget was higher than maximum budget, so I swapped them.")

    target_budget = (min_budget + max_budget) / 2

    use_cases = []
    if wants_office:
        use_cases.append("office")
    if wants_gaming:
        use_cases.append("gaming")
        use_cases.append("creator")
    if wants_home:
        use_cases.append("home")

    for use_case in guess_use_cases(user_text):
        if use_case not in use_cases:
            use_cases.append(use_case)

    if not use_cases:
        use_cases = ["home"]

    preferences = get_preferences(max_budget)

    if st.button("Build My PC"):
        build = find_best_pc(use_cases, min_budget, max_budget, preferences)

        st.header("Recommended PC Build")
        st.write(f"Budget range used: {rupees(min_budget)} to {rupees(max_budget)}")
        st.metric("Estimated midpoint total", rupees(build["total_price"]))
        st.write(
            "Real checkout price can change by shop, sale, stock, delivery, and card offer. "
            "Use the shop buttons on each part before buying."
        )

        if build["total_price"] < min_budget:
            st.warning("This build is below your lower bound because the selected requirements do not need more spending.")
        if build["total_price"] > max_budget:
            st.warning("This build is above your upper bound because the requirements are too tight.")

        processor = find_part(build["parts"], "Processor")
        graphics_card = find_part(build["parts"], "Graphics Card")
        st.write(
            f"Processor fuzzy fit: {processor_fuzzy_score(processor, use_cases, target_budget, preferences['cpu_priority']):.1f}"
        )
        st.write(
            f"GPU fuzzy fit: {gpu_fuzzy_score(graphics_card, use_cases, target_budget, preferences['gpu_need']):.1f}"
        )

        col1, col2 = st.columns(2)
        for index, part in enumerate(build["parts"]):
            alternatives = build["alternatives"].get(part["category"], [])
            with col1 if index % 2 == 0 else col2:
                show_part_card(part, alternatives)
                st.divider()

    st.divider()
    st.caption(
        "Photo previews are reference images. Shopping buttons open live search pages so users can compare actual price and availability."
    )

PRODUCTS.extend(
    [
        {"category": "Wi-Fi Card", "name": "TP-Link Archer TXE75E Wi-Fi 6E", "price": 4200, "office": 82, "gaming": 82, "home": 84, "creator": 80, "wifi_rank": 76, "details": "PCIe card, Wi-Fi 6E with 6GHz support"},
        {"category": "Wi-Fi Card", "name": "ASUS PCE-AXE58BT Wi-Fi 6E", "price": 5200, "office": 84, "gaming": 84, "home": 86, "creator": 82, "wifi_rank": 80, "details": "Wi-Fi 6E PCIe card with Bluetooth"},
        {"category": "Wi-Fi Card", "name": "Gigabyte GC-WBAX210 Wi-Fi 6E", "price": 4500, "office": 82, "gaming": 84, "home": 84, "creator": 82, "wifi_rank": 78, "details": "Wi-Fi 6E class PCIe card"},
        {"category": "Wi-Fi Card", "name": "MSI Herald-BE NCM865 Wi-Fi 7", "price": 7900, "office": 90, "gaming": 92, "home": 90, "creator": 90, "wifi_rank": 94, "details": "Wi-Fi 7 card, above Wi-Fi 6E"},
        {"category": "Wi-Fi Card", "name": "TP-Link Archer TBE550E Wi-Fi 7", "price": 8200, "office": 92, "gaming": 94, "home": 92, "creator": 92, "wifi_rank": 96, "details": "Fast Wi-Fi 7 PCIe card"},
        {"category": "Power Supply", "name": "450W 80+ Bronze PSU", "price": 2800, "office": 72, "gaming": 46, "home": 70, "creator": 44, "capacity": 450, "quality": 55, "details": "450W, only for low-power builds"},
        {"category": "Power Supply", "name": "550W 80+ Bronze PSU", "price": 3900, "office": 80, "gaming": 72, "home": 78, "creator": 70, "capacity": 550, "quality": 68, "details": "550W, mainstream budget PSU"},
        {"category": "Power Supply", "name": "650W 80+ Gold PSU", "price": 6100, "office": 88, "gaming": 86, "home": 82, "creator": 84, "capacity": 650, "quality": 84, "details": "650W Gold, good upgrade room"},
        {"category": "Power Supply", "name": "750W 80+ Gold PSU", "price": 8100, "office": 90, "gaming": 92, "home": 84, "creator": 90, "capacity": 750, "quality": 90, "details": "750W Gold, strong GPU headroom"},
        {"category": "Power Supply", "name": "850W 80+ Gold PSU", "price": 10500, "office": 92, "gaming": 96, "home": 86, "creator": 96, "capacity": 850, "quality": 96, "details": "850W Gold, high-end GPU friendly"},
        {"category": "Cabinet", "name": "Airflow mATX Cabinet", "price": 2600, "office": 72, "gaming": 62, "home": 74, "creator": 62, "supported_sizes": ["mATX"], "airflow": 60, "details": "Compact mATX case with basic airflow"},
        {"category": "Cabinet", "name": "Mid Tower Airflow Cabinet", "price": 4300, "office": 82, "gaming": 82, "home": 80, "creator": 80, "supported_sizes": ["mATX", "ATX"], "airflow": 78, "details": "Good airflow and cable space"},
        {"category": "Cabinet", "name": "Creator Mid Tower Cabinet", "price": 7200, "office": 88, "gaming": 90, "home": 82, "creator": 92, "supported_sizes": ["mATX", "ATX"], "airflow": 90, "details": "Quiet fans, USB-C, large GPU room"},
    ]
)

PRODUCTS.extend(
    [
        {"category": "RAM", "name": "8GB DDR4 3200MHz", "price": 1600, "office": 66, "gaming": 42, "home": 68, "creator": 36, "ram_type": "DDR4", "gb": 8, "details": "8GB DDR4, only for strict low budget"},
        {"category": "RAM", "name": "16GB DDR4 3200MHz", "price": 3100, "office": 84, "gaming": 76, "home": 82, "creator": 68, "ram_type": "DDR4", "gb": 16, "details": "16GB DDR4, basic gaming and daily use"},
        {"category": "RAM", "name": "32GB DDR4 3200MHz", "price": 6200, "office": 92, "gaming": 88, "home": 86, "creator": 86, "ram_type": "DDR4", "gb": 32, "details": "32GB DDR4, editing friendly"},
        {"category": "RAM", "name": "16GB DDR5 5600MHz", "price": 5100, "office": 88, "gaming": 82, "home": 84, "creator": 76, "ram_type": "DDR5", "gb": 16, "details": "16GB DDR5, modern platform"},
        {"category": "RAM", "name": "32GB DDR5 6000MHz", "price": 9800, "office": 96, "gaming": 94, "home": 90, "creator": 94, "ram_type": "DDR5", "gb": 32, "details": "32GB DDR5, best for high budget builds"},
        {"category": "RAM", "name": "32GB LPDDR5X Integrated Memory", "price": 0, "office": 94, "gaming": 42, "home": 88, "creator": 72, "ram_type": "LPDDR5X", "gb": 32, "details": "Integrated Snapdragon memory"},
        {"category": "ROM / Storage", "name": "256GB NVMe SSD", "price": 1500, "office": 62, "gaming": 35, "home": 58, "creator": 30, "storage_gb": 256, "details": "256GB NVMe, only for strict low budget"},
        {"category": "ROM / Storage", "name": "512GB NVMe SSD", "price": 2600, "office": 76, "gaming": 62, "home": 76, "creator": 54, "storage_gb": 512, "details": "512GB NVMe, light use"},
        {"category": "ROM / Storage", "name": "1TB NVMe SSD", "price": 5200, "office": 88, "gaming": 86, "home": 86, "creator": 82, "storage_gb": 1024, "details": "1TB NVMe, best default"},
        {"category": "ROM / Storage", "name": "2TB NVMe SSD", "price": 10200, "office": 92, "gaming": 94, "home": 90, "creator": 94, "storage_gb": 2048, "details": "2TB NVMe, games and large projects"},
        {"category": "Graphics Card", "name": "Integrated Graphics", "brand": "Integrated", "price": 0, "office": 70, "gaming": 12, "home": 72, "creator": 32, "wattage": 0, "speed": 20, "details": "No separate GPU"},
        {"category": "Graphics Card", "name": "AMD Radeon RX 7600 XT 16GB", "brand": "AMD", "price": 32500, "office": 78, "gaming": 78, "home": 72, "creator": 74, "wattage": 190, "speed": 70, "details": "16GB VRAM, value 1080p/entry 1440p"},
        {"category": "Graphics Card", "name": "AMD Radeon RX 9060 XT 8GB", "brand": "AMD", "price": 31500, "office": 80, "gaming": 82, "home": 74, "creator": 76, "wattage": 150, "speed": 76, "details": "Recent mainstream Radeon GPU"},
        {"category": "Graphics Card", "name": "AMD Radeon RX 9060 XT 16GB", "brand": "AMD", "price": 37500, "office": 82, "gaming": 86, "home": 76, "creator": 82, "wattage": 160, "speed": 80, "details": "Recent Radeon with more VRAM"},
        {"category": "Graphics Card", "name": "AMD Radeon RX 9070 16GB", "brand": "AMD", "price": 56500, "office": 86, "gaming": 94, "home": 80, "creator": 90, "wattage": 220, "speed": 92, "details": "High-performance Radeon GPU"},
        {"category": "Graphics Card", "name": "AMD Radeon RX 9070 XT 16GB", "brand": "AMD", "price": 69000, "office": 88, "gaming": 98, "home": 82, "creator": 94, "wattage": 304, "speed": 98, "details": "Fast AMD gaming and creator GPU"},
        {"category": "Graphics Card", "name": "AMD Radeon AI PRO R9700 32GB", "brand": "AMD", "price": 98000, "office": 90, "gaming": 92, "home": 80, "creator": 99, "wattage": 300, "speed": 96, "details": "AMD creator/workstation style GPU"},
    ]
)
if __name__ == "__main__":
    run_app()
