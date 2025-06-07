#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from collections import defaultdict
import random
import pandas as pd

if 'checked_items' not in st.session_state:
    st.session_state.checked_items = {}

# ----- Define Recipes with units and optional tags -----
# Format: ingredient: (quantity, unit)
recipes = {
    "Pasta Bolognese": {
        "Spaghetti": (2, "servings"),
        "Minced beef": (200, "grams"),
        "Bolognese Sauce": (1, "cup"),
        "Onion": (1, "pieces"),
        "Mushroom": (5, "pieces"),
        "Cheese": (1, "slices")
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
        "Meat": (2, "servings")
    },
    "Bokkeumbap": {
        "Mushroom": (6, "pieces"),
        "Sesame Oil": (1, "tbsp"),
        "Onion": (1, "pieces"),
        "Garlic": (1, "clove"),
        "Broccoli": (0.5, "pieces"),
        "Eggs": (2, "pieces"),
        "Meat": (2, "servings"),
        "_tags": ["leftover"]
    },
    "Carbonara": {
        "Mushroom": (5, "pieces"),
        "Spaghetti": (2, "servings"),
        "Bacon/Ham": (2, "slices"),
        "Chicken Stock": (1, "cubes"),
        "Milk": (0.25, "cups"),
        "Onion": (1, "pieces")
    },
    "Casserole": {
        "Mushroom": (6, "pieces"),
        "Butter": (1, "tbsp"),
        "Milk": (0.5, "cups"),
        "Garlic": (1, "clove"),
        "Onion": (1, "pieces"),
        "Chicken Stock": (1, "cubes"),
        "Flour": (2, "tbsp"),
        "Cheese": (2, "slices"),
        "Broccoli": (0.5, "pieces"),
        "Meat": (2, "servings"),
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
        "Fish/Meatball": (4,"pieces")
    },
    "Indomee": {
        "Indomee": (2,"packets"),
        "Onion": (1,"pieces"),
        "Eggs": (1,"pieces"),
        "Meat": (2,"servings")
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
        "Flour": (0.5,"tsp")
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
        "Capsicum":(1,"cup")
    },
    "Jap Curry Omurice": {
        "Garlic": (1, "clove"),
        "Onion": (1,"pieces"),
        "Baby Potato": (2,"pieces"),
        "Chicken Fillet": (2, "servings"),
        "Fish Sauce": (1,"tbsp"),
        "Jap Curry Cubes": (1.5,"cubes"),
        "Eggs": (2,"pieces"),
        "_tags": ["leftover"]
    }
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MEALS = ["Lunch", "Dinner"]

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
    must_include_meals = st.multiselect("Choose meals to include this week:", list(recipes.keys()))

    st.markdown("### 🚫 Meals Eaten Out")
    meals_eaten_out = {}
    for day in DAYS:
        cols = st.columns(2)
        for i, meal in enumerate(MEALS):
            key = f"out_{day}_{meal}"
            if cols[i].checkbox(f"{day} {meal}", key=key):
                meals_eaten_out.setdefault(day, []).append(meal)

    if st.button("🔁 Generate Meal Plan"):
        total_slots = 14
        meals_out_count = sum(len(v) for v in meals_eaten_out.values())
        meals_to_plan = total_slots - meals_out_count

        available_meals = list(set(recipes.keys()) - set(must_include_meals))
        random.shuffle(available_meals)
        needed = meals_to_plan - len(must_include_meals)
        selected_meals = must_include_meals + random.choices(available_meals, k=needed)
        random.shuffle(selected_meals)

        plan = {}
        pool = selected_meals.copy()

        for i, day in enumerate(DAYS):
            plan[day] = {}
            for j, meal in enumerate(MEALS):
                if meal in meals_eaten_out.get(day, []):
                    plan[day][meal] = "Eating Out"
                elif i > 0 and meal == "Lunch":
                    prev_dinner = plan[DAYS[i - 1]]["Dinner"]
                    if prev_dinner in recipes and "_tags" in recipes[prev_dinner] and "leftover" in recipes[prev_dinner]["_tags"]:
                        plan[day][meal] = prev_dinner
                    else:
                        plan[day][meal] = pool.pop() if pool else "No Meal Planned"
                else:
                    plan[day][meal] = pool.pop() if pool else "No Meal Planned"

        grocery_list = defaultdict(lambda: defaultdict(float))
        for day in DAYS:
            for meal in MEALS:
                m = plan[day][meal]
                if m not in ("Eating Out", "No Meal Planned"):
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
