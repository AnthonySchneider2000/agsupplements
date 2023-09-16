export interface Item {
  id: number;
  name: string;
  description: string;
  price: number;
}

export interface Ingredient {
  id: number;
  name: string;
  description: string;
  price: number;
}

export interface ItemWithIngredients {
  id: number;
  name: string;
  description: string;
  price: number;
  ingredients: ItemIngredient[];
}

export interface ItemIngredient {
  id: number;
  item: ItemWithIngredients;
  ingredient: Ingredient;
  mass: number;
}
