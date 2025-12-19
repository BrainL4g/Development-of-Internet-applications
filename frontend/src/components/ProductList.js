import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ProductCard from './ProductCard';
import ProductForm from './ProductForm';

const API_URL = 'http://localhost:8000/products';

function ProductList() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(API_URL);
      setProducts(response.data);
    } catch (error) {
      console.error('Ошибка загрузки товаров:', error);
    }
  };

  const addProduct = async (data) => {
    const formData = new FormData();
    formData.append('name', data.name);
    if (data.description) formData.append('description', data.description);
    formData.append('price', data.price);
    formData.append('stock', data.stock);

    try {
      await axios.post(API_URL, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      fetchProducts();
    } catch (error) {
      console.error('Ошибка добавления товара:', error);
    }
  };

  const updateProduct = async (updated) => {
    try {
      await axios.put(`${API_URL}/${updated.id}`, updated);
      fetchProducts();
    } catch (error) {
      console.error('Ошибка обновления товара:', error);
    }
  };

  const deleteProduct = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchProducts();
    } catch (error) {
      console.error('Ошибка удаления товара:', error);
    }
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