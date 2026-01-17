// tests/unit/lib/api/client.test.ts
// Testes para API Client são melhor feitos em integração
// devido à complexidade de mockar axios singleton

import { apiClient } from '@/lib/api/client';

describe('ApiClient', () => {
  it('is exported correctly', () => {
    expect(apiClient).toBeDefined();
  });

  it('has required methods', () => {
    expect(apiClient).toHaveProperty('get');
    expect(apiClient).toHaveProperty('post');
    expect(apiClient).toHaveProperty('put');
    expect(apiClient).toHaveProperty('delete');
    expect(typeof apiClient.get).toBe('function');
    expect(typeof apiClient.post).toBe('function');
    expect(typeof apiClient.put).toBe('function');
    expect(typeof apiClient.delete).toBe('function');
  });
});
