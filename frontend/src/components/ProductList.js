import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ProductCard from './ProductCard';
import ProductForm from './ProductForm';

function ProductList() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    setProducts([
      { id: uuidv4(), name: 'iPhone 15 Pro', description: 'Флагманский смартфон Apple', price: 129990, stock: 10 },
      { id: uuidv4(), name: 'Samsung Galaxy S24 Ultra', description: 'Топовый Android-смартфон', price: 119990, stock: 8 },
      { id: uuidv4(), name: 'MacBook Air M3', description: 'Лёгкий и мощный ноутбук', price: 149990, stock: 5 },
      { id: uuidv4(), name: 'Sony WH-1000XM5', description: 'Премиальные наушники с ANC', price: 34990, stock: 20 },
    ]);
  }, []);

  const addProduct = (data) => {
    setProducts(prev => [...prev, { id: uuidv4(), ...data }]);
  };

  const updateProduct = (updated) => {
    setProducts(prev => prev.map(p => p.id === updated.id ? updated : p));
  };

  const deleteProduct = (id) => {
    setProducts(prev => prev.filter(p => p.id !== id));
  };

  return (
    <div>
      <div className="admin-section">
        <h2>Добавить новый товар</h2>
        <ProductForm onSubmit={addProduct} />
      </div>

      <h2 className="catalog-title">Каталог товаров</h2>
      <div className="products-grid">
        {products.map(product => (
          <ProductCard
            key={product.id}
            product={product}
            onUpdate={updateProduct}
            onDelete={deleteProduct}
          />
        ))}
      </div>
    </div>
  );
}

export default ProductList;