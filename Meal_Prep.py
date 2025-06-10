#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from collections import defaultdict, Counter
import random
import pandas as pd

if 'checked_items' not in st.session_state:
    st.session_state.checked_items = {}

# ----- Define Recipes with units and optional tags -----
# Format: ingredient: (quantity, unit)
# Added tags for 'dinner_only' and 'light_meal' where appropriate
recipes = {
    "Pasta Bolognese": {
        "Spaghetti": (2, "servings"),
        "Minced beef": (200, "grams"),
        "Bolognese Sauce": (1, "cup"),
        "Onion": (1, "pieces"),
        "Mushroom": (5, "pieces"),
        "Cheese": (1, "slices"),
        "_tags": ["dinner_only"]
    },
    "Egg Onion Rice": {
        "Eggs": (2, "pieces"),
        "Onion": (1, "pieces"),
        "Broccoli": (0.5, "pieces"),
        "Meat": (2, "servings"),
        "Rice": (0.75, "cups"),
        "_tags": ["leftover"]
    },
    "Creamy Mushroom": {
        "Mushroom": (6, "pieces"),
        "Butter": (1, "tbsp"),
        "Milk": (0.5, "cups"),
        "Garlic": (1, "tbsp"),
        "Onion": (1, "pieces"),
        "Chicken Stock": (1, "cubes"),
        "Flour": (2, "tbsp"),
        "Meat": (2, "servings"),
        "_tags": ["leftover"]
    },
    "Bokkeumbap": {
        "Mushroom": (6, "pieces"),
        "Sesame Oil": (1, "tbsp"),
        "Onion": (1, "pieces"),
        "Garlic": (1, "clove"),
        "Broccoli": (0.5, "pieces"),
        "Eggs": (2, "pieces"),
        "Meat": (2, "servings"),
        "Rice": (0.75,"cups"),
        "_tags": ["leftover"]
    },
    "Carbonara": {
        "Mushroom": (5, "pieces"),
        "Spaghetti": (2, "servings"),
        "Bacon/Ham": (2, "slices"),
        "Chicken Stock": (1, "cubes"),
        "Milk": (0.25, "cups"),
        "Onion": (1, "pieces"),
        "_tags": ["dinner_only"]
    },
    "Casserole": {
        "Mushroom": (6, "pieces"),
        "Butter": (1, "tbsp"),
        "Milk": (0.5, "cups"),
        "Garlic": (1, "clove"),
        "Onion": (1, "pieces"),
        "Chicken Stock": (1, "cubes"),
        "Flour": (2, "tbsp"),
        "Cheese": (4, "slices"),
        "Broccoli": (0.5, "pieces"),
        "Meat": (2, "servings"),
        "Rice": (0.75,"cups"),
        "_tags": ["leftover"]
    },
    "Dashi Noodles":{
        "Noodles": (2, "servings"),
        "Dashi": (1, "packets"),
        "Mirin": (1, "tbsp"),
        "Light Soy Sauce": (1,"tbsp"),
        "Sugar": (1,"tsp"),
        "Onion": (1,"pieces"),
        "Broccoli": (0.5,"pieces"),
        "Bacon/Ham": (2,"slices"),
        "Fish/Meatball": (4,"pieces"),
        "_tags": ["dinner_only"]
    },
    "Indomee": {
        "Indomee": (2,"packets"),
        "Onion": (1,"pieces"),
        "Eggs": (1,"pieces"),
        "Meat": (2,"servings"),
        "_tags": ["dinner_only"]
    },
    "Stir-Fry Noodles":{
        "Noodles": (2,"servings"),
        "Meat": (2,"servings"),
        "Onion": (1,"pieces"),
        "Boy Choy": (1,"pieces"),
        "Mirin": (2,"tbsp"),
        "Dark Soy Sauce": (1,"tbsp"),
        "Light Soy Sauce": (2,"tbsp"),
        "Sugar": (1,"tbsp"),
        "Sesame Oil": (1,"tsp"),
        "Flour": (0.5,"tsp"),
        "_tags": ["dinner_only"]
    },
    "Japchae": {
        "Light Soy Sauce": (4,"tbsp"),
        "Sugar": (2,"tbsp"),
        "Sesame Oil": (2,"tbsp"),
        "Mushroom": (5,"pieces"),
        "Onion": (1,"pieces"),
        "Broccoli": (0.5,"pieces"),
        "Eggs": (2,"pieces"),
        "Meat": (2,"servings"),
        "Capsicum":(1,"cup"),
        "_tags": ["dinner_only"]
    },
    "Jap Curry Omurice": {
        "Garlic": (1, "clove"),
        "Onion": (1,"pieces"),
        "Baby Potato": (2,"pieces"),
        "Chicken Fillet": (2, "servings"),
        "Fish Sauce": (1,"tbsp"),
        "Jap Curry Cubes": (1.5,"cubes"),
        "Eggs": (2,"pieces"),
        "Rice": (0.75,"cups"),
        "_tags": ["leftover"]
    },
    "Crackers and Dip": {
        "Crackers": (1,"piece"),
        "Dip": (1,"piece"),
        "_tags": ["light_meal"]
    },
    "Big Breakfast": {
        "Hashbrown": (2,"pieces"),
        "Eggs": (2,"pieces"),
        "Chicken Fillet": (2, "pieces"),
        "_tags": ["lunch_only"]
    },
    "Seafood Bites": {
        "Seafood Bites": (8,"pieces"),
        "Broccoli": (0.5,"pieces"),
        "Squid Ball": (4,"pieces"),
        "Rice": (0.75,"cups"),
        "_tags": ["dinner_only"]
    }
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MEALS = ["Lunch", "Dinner"]
MAX_REPETITION = 3



# -------------------- Styling --------------------
st.markdown("""
<style>
    .stCheckbox > label {
        font-size: 0.9rem;
    }
    .stApp {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- Session State --------------------
if "generate" not in st.session_state:
    st.session_state.generate = False
if "week_plan" not in st.session_state:
    st.session_state.week_plan = {}
if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = {}
if "checked_items" not in st.session_state:
    st.session_state.checked_items = {}

# -------------------- App Layout --------------------
st.title("🥗 Weekly Meal Planner")
tab1, tab2, tab3 = st.tabs(["📅 Meal Plan", "🛒 Grocery List", "⚙️ Settings"])

with tab3:
    st.markdown("### ✅ Must-Include Meals")
    must_include_meals = st.multiselect("Choose meals to include this week:", sorted(recipes.keys()))

    st.markdown("### 🚫 Meals Eaten Out")
    meals_eaten_out = {}
    for day in DAYS:
        cols = st.columns(2)
        for i, meal in enumerate(MEALS):
            key = f"out_{day}_{meal}"
            if cols[i].checkbox(f"{day} {meal}", key=key):
                meals_eaten_out.setdefault(day, []).append(meal)

    # Initialize session_state for preselected meals (runs once per session)
    if "preselected_meals" not in st.session_state:
        st.session_state.preselected_meals = {
            day: {meal: None for meal in MEALS} for day in DAYS
        }
    else:
        # Defensive check: fill missing days or meals if any
        for day in DAYS:
            if day not in st.session_state.preselected_meals:
                st.session_state.preselected_meals[day] = {meal: None for meal in MEALS}
            else:
                for meal in MEALS:
                    if meal not in st.session_state.preselected_meals[day]:
                        st.session_state.preselected_meals[day][meal] = None

    # UI for preselecting meals
    st.markdown("### 📝 Preselect Meals for Specific Days")
    sorted_recipes = sorted(recipes.keys())
    
    for day in DAYS:
        with st.expander(day):
            cols = st.columns(len(MEALS))
            for i, meal in enumerate(MEALS):
                key = f"preselect_{day}_{meal}"
                current_val = st.session_state.preselected_meals[day][meal]
                
                if current_val in recipes:
                    index = sorted_recipes.index(current_val) + 1 if current_val in sorted_recipes else 0
                else:
                    index = 0

                choice = cols[i].selectbox(
                    f"{meal}",
                    options=[None] + sorted_recipes,
                    index=index,
                    key=key,
                )


                # Update the nested dict in session_state safely
                day_meals = st.session_state.preselected_meals[day].copy()
                day_meals[meal] = choice
                st.session_state.preselected_meals[day] = day_meals
                
    if st.button("🔁 Generate Meal Plan"):
        total_slots = 14
        meals_out_count = sum(len(v) for v in meals_eaten_out.values())
        meals_to_plan = total_slots - meals_out_count

        # Build set of meals to exclude from random pool:
        # Exclude light meals for random assignment
        light_meals = {m for m, r in recipes.items() if "_tags" in r and "light_meal" in r["_tags"]}
        dinner_only_meals = {m for m, r in recipes.items() if "_tags" in r and "dinner_only" in r["_tags"]}

        # Pool of meals to choose from (exclude must_include, light meals)
        pool_meals = set(recipes.keys()) - set(must_include_meals) - light_meals

        # For dinner slots, pool includes dinner_only meals + other meals in pool_meals
        # For lunch slots, exclude dinner_only meals

        # Prepare list to track repetition counts
        repetition_counter = Counter()

        # Start building plan dict with preselected meals first, then fill others
        plan = {}
        # First count preselected meals repetition, ignore None
        for day in DAYS:
            for meal_time in MEALS:
                sel_meal = st.session_state.preselected_meals[day][meal_time]
                if sel_meal:
                    repetition_counter[sel_meal] += 1

        # Include must_include meals in repetition count as well, so they don't exceed max repetition
        # We will randomly assign must_include meals after preselected assignments
        for meal in must_include_meals:
            repetition_counter[meal] += 0  # Just initialize if not present

        # Prepare a helper function to get next meal for slot respecting constraints
        def get_next_meal_for_slot(meal_time):
            if meal_time == "Dinner":
                candidates = [
                    m for m in pool_meals.union(dinner_only_meals)
                    if repetition_counter[m] < MAX_REPETITION
                    and "lunch_only" not in recipes[m].get("_tags", [])
                ]
            else:  # Lunch
                candidates = [
                    m for m in pool_meals
                    if m not in dinner_only_meals
                    and repetition_counter[m] < MAX_REPETITION
                ]
            if not candidates:
                return None
            return random.choice(candidates)


        # Start filling the plan
        # Steps:
        # 1) Put preselected meals in place
        # 2) Insert must_include meals randomly in leftover slots
        # 3) Fill remaining slots with random allowed meals

        # 1) Setup plan with preselected or placeholders
        for day in DAYS:
            plan[day] = {}
            for meal_time in MEALS:
                pre_sel = st.session_state.preselected_meals[day][meal_time]
                if meal_time in meals_eaten_out.get(day, []):
                    plan[day][meal_time] = "Eating Out"
                elif pre_sel:
                    plan[day][meal_time] = pre_sel
                else:
                    plan[day][meal_time] = None  # placeholder for assignment

        # 2) Assign must_include meals randomly to None slots
        # Shuffle must_include meals and assign without exceeding repetition limit
        must_include_pool = must_include_meals.copy()
        random.shuffle(must_include_pool)

        for meal in must_include_pool:
            assigned = 0
            for day in DAYS:
                for meal_time in MEALS:
                    if assigned >= 1:
                        break
                    if plan[day][meal_time] is None and repetition_counter[meal] < MAX_REPETITION:
                        # Check if dinner_only tag restricts slot
                        tags = recipes[meal].get("_tags", [])
                        if "dinner_only" in tags and meal_time != "Dinner":
                            continue
                        if "lunch_only" in tags and meal_time != "Lunch":
                            continue
                        plan[day][meal_time] = meal
                        repetition_counter[meal] += 1
                        assigned += 1
            # If we run out of slots for must_include meal (rare), it won't be assigned fully

        # 3) Fill remaining None slots
        for day in DAYS:
            for meal_time in MEALS:
                if plan[day][meal_time] is None:
                    meal_choice = get_next_meal_for_slot(meal_time)
                    if meal_choice:
                        plan[day][meal_time] = meal_choice
                        repetition_counter[meal_choice] += 1
                    else:
                        plan[day][meal_time] = "No Meal Planned"

        # 4) Handle leftover lunch assignment logic (same as original)
        for i, day in enumerate(DAYS):
            # Only if lunch is not preselected or Eating Out
            if plan[day]["Lunch"] in (None, "No Meal Planned") and day != DAYS[0]:
                prev_dinner = plan[DAYS[i - 1]]["Dinner"]
                if prev_dinner in recipes and "_tags" in recipes[prev_dinner] and "leftover" in recipes[prev_dinner]["_tags"]:
                    plan[day]["Lunch"] = prev_dinner

        # Calculate grocery list
        grocery_list = defaultdict(lambda: defaultdict(float))
        for day in DAYS:
            for meal_time in MEALS:
                m = plan[day][meal_time]
                if m not in ("Eating Out", "No Meal Planned", None):
                    for ing, val in recipes[m].items():
                        if ing == "_tags":
                            continue
                        qty, unit = val
                        grocery_list[ing][unit] += qty

        st.session_state.week_plan = plan
        st.session_state.grocery_list = grocery_list
        st.session_state.checked_items = {}
        st.session_state.generate = True

with tab1:
    if st.session_state.generate:
        st.subheader("🗓️ Weekly Meal Plan")

        def make_plan_df(plan):
            data = {day: [plan[day]["Lunch"], plan[day]["Dinner"]] for day in DAYS}
            return pd.DataFrame(data, index=["Lunch", "Dinner"]).T

        df = make_plan_df(st.session_state.week_plan)
        st.dataframe(df, use_container_width=True)
        
with tab2:
    if st.session_state.grocery_list:
        st.subheader("🛒 Grocery List (Check Items Off – Sorted)")

        items = []
        for ing, unit_dict in st.session_state.grocery_list.items():
            for unit, qty in unit_dict.items():
                qty_disp = int(qty) if qty.is_integer() else round(qty, 2)
                key = f"{ing}_{unit}"
                checked = st.session_state.checked_items.get(key, False)
                items.append((checked, ing, unit, qty_disp, key))

        items.sort(key=lambda x: (x[0], x[1]))

        st.markdown("### ✅ To Buy")
        for checked, ing, unit, qty_disp, key in items:
            if not checked:
                st.session_state.checked_items[key] = st.checkbox(
                    f"{ing}: {qty_disp} {unit}", key=key, value=checked
                )

        st.markdown("---\n### ✔️ Bought")
        for checked, ing, unit, qty_disp, key in items:
            if checked:
                st.session_state.checked_items[key] = st.checkbox(
                    f"~~{ing}: {qty_disp} {unit}~~", key=key, value=checked
                )
                
                
import io

if st.session_state.generate and st.session_state.grocery_list:
    # Meal Plan CSV section
    meal_csv = df.to_csv(index=True, index_label="Day")

    # Grocery List: only include items not checked off as "bought"
    grocery_items = []
    for ing, unit_dict in st.session_state.grocery_list.items():
        for unit, qty in unit_dict.items():
            key = f"{ing}_{unit}"
            checked = st.session_state.checked_items.get(key, False)
            if not checked:  # To Buy only
                qty_disp = int(qty) if qty.is_integer() else round(qty, 2)
                grocery_items.append({
                    "Ingredient": ing,
                    "Quantity": qty_disp,
                    "Unit": unit
                })

    # Convert grocery items to CSV
    grocery_items.sort(key=lambda x: x["Ingredient"])  # Sort alphabetically
    grocery_df = pd.DataFrame(grocery_items)
    grocery_csv = grocery_df.to_csv(index=False)

    # Combine both sections into one string
    combined_csv = io.StringIO()
    combined_csv.write("Meal Plan\n")
    combined_csv.write(meal_csv)
    combined_csv.write("\nGrocery List\n")
    combined_csv.write(grocery_csv)

    # Encode for download
    combined_csv.seek(0)
    csv_data = combined_csv.getvalue().encode('utf-8')

    st.download_button(
        label="📥 Download Combined Meal Plan & Grocery List (CSV)",
        data=csv_data,
        file_name="meal_and_grocery.csv",
        mime="text/csv"
    )
