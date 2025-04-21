export interface Tags {
  id: number;
  name: string;
  description: string;
}

export let tags_list = [
  {
    id: 1,
    name: 'python',
    description:
      'Python is a multi-paradigm, dynamically typed, multi-purpose programming language. It is designed to be quick to learn, understand, and use, and enforces a clean and uniform syntax. Please note that Python 2 is officially out of support as of 2020-01-01. For version-specific Python questions, add the [python-2.7] or [python-3.x] tag. When using a Python variant (e.g. Jython, PyPy) or library (e.g. Pandas, NumPy), please include it in the tags.',
  },
  {
    id: 2,
    name: 'web',
    description:
      'Do not use this tag. For questions related to an aspect of the world wide web, use a more specific tag for it, such as [uri], [html], [http] or [w3c].',
  },
  {
    id: 3,
    name: 'basics',
    description: 'General tag for basic coding',
  },
];
