import { describe, expect, it } from 'vitest';

import { cn } from './utils';

describe('cn', () => {
  it('merges conditional class names and resolves tailwind conflicts', () => {
    expect(cn('rounded-md px-2', false && 'hidden', 'px-4')).toBe('rounded-md px-4');
  });
});
