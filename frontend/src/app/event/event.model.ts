export interface Event {
    id: number;
    type: string; // Football, Basketball и т.п.
    place: string;
    date: string; // ISO-формат, например: 2025-04-21T18:00:00Z
    description: string;
    capacity: number;
    isActive: boolean;
    creator: number; // id участника-создателя
    can_apply: boolean; // приходит из кастомного retrieve
    image?: string;
  }
  