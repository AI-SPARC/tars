import { describe, expect, it } from 'vitest';

import { cn } from './utils';

describe('cn', () => {
  it('merges conditional class names and resolves tailwind conflicts', () => {
    const hidden = false;
    expect(cn('rounded-md px-2', hidden ? 'hidden' : undefined, 'px-4')).toBe('rounded-md px-4');
  });
});
