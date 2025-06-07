export type foodType = {
  id: number;
  side_fishes: [
    {
      id: number;
      name: string;
      is_active: true;
      created_at: string;
      updated_at: string;
      foods: number[];
    }
  ];
  predefined_food: {
    id: number;
    name: string;
    food_type: string;
    description: string;
  };
  custom_name: string;
  food_type: string;
  description: string;
  food_date: number;
};

export type groupFoodType = [
  string,
  [
    {
      id: number;
      foods: foodType[];
      jdate: string;
      user_reserved_ids: [];
      can_reserve: true;
      date: string;
    }
  ]
][];

export type reserveType = {
  id: number;
  jcreated_at: string;
  date: string;
  created_at: string;
  is_delivered: false;
  food: number;
};
