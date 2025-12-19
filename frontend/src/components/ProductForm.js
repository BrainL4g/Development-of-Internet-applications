import React, { useState, useEffect } from 'react';

function ProductForm({ product, onSubmit, onCancel }) {
  const [form, setForm] = useState({ name: '', description: '', price: '', stock: '' });

  useEffect(() => {
    if (product) {
      setForm({
        name: product.name,
        description: product.description || '',
        price: product.price,
        stock: product.stock
      });
    }
  }, [product]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      name: form.name.trim(),
      description: form.description.trim() || null,
      price: Number(form.price),
      stock: Number(form.stock || 0)
    });
    if (!product) {
      setForm({ name: '', description: '', price: '', stock: '' });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <input name="name" placeholder="Название *" value={form.name} onChange={handleChange} required />
      <textarea name="description" placeholder="Описание" value={form.description} onChange={handleChange} />
      <input name="price" type="number" placeholder="Цена *" value={form.price} onChange={handleChange} required />
      <input name="stock" type="number" placeholder="На складе" value={form.stock} onChange={handleChange} min="0" />
      <div className="form-buttons">
        <button type="submit">{product ? 'Сохранить' : 'Добавить'}</button>
        {onCancel && <button type="button" onClick={onCancel}>Отмена</button>}
      </div>
    </form>
  );
}

export default ProductForm;