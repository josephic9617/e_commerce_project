<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <span class="brand-icon">&#9830;</span>
        <span>E-Shop</span>
      </div>
      <p class="footer-text">&copy; 2026 E-Shop. {{ $t('all_rights') }}</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: auto;
  padding: 24px 0;
  border-top: 1px solid var(--border);
  background: var(--bg-secondary);
}

.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 18px;
  color: var(--primary);
}

.brand-icon {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.footer-text {
  font-size: 13px;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .footer-inner {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}
</style>
