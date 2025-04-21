import { Messages } from './messages';

export interface Questions {
  id: number;
  title: string;
  body: string;
  user: number;
  tag: number;
  created: Date;
  updated: Date;
  is_active: boolean;
  code_field: string;
}

export let question_list = [
  {
    id: 1,
    title: 'How to sum a list in Python?',
    body: 'Hello guys! I am new to Python and do not know how tp sum a list. Can anybody help me?',
    user: 1,
    tag: 1,
    created_date: new Date('2022-01-17T15:24:00'),
    updated_date: new Date('2022-01-17T15:34:10'),
    is_active: true,
    code_field: '',
  },
  {
    id: 2,
    title: 'How to activate virtual environment?',
    body: 'Hi! How to activate newly created venv?',
    user: 2,
    tag: 3,
    created_date: new Date('2022-01-21T12:21:00'),
    updated_date: new Date('2022-01-21T12:23:45'),
    is_active: false,
    code_field: '',
  },
];
