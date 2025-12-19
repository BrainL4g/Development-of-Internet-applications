import React, { useState } from 'react';
import ProductForm from './ProductForm';

function ProductItem({ product, onUpdate, onDelete }) {
  const [editing, setEditing] = useState(false);

  const save = (data) => {
    onUpdate({ ...product, ...data });
    setEditing(false);
  };

  if (editing) {
    return (
      <div className="item edit-mode">
        <ProductForm product={product} onSubmit={save} onCancel={() => setEditing(false)} />
      </div>
    );
  }

  return (
    <div className="item">
      <div className="item-image">
        {product.name.includes('iPhone') || product.name.includes('Samsung') ? '📱' :
         product.name.includes('MacBook') ? '💻' :
         product.name.includes('Sony') ? '🎧' : '🔌'}
      </div>
      <div className="item-content">
        <h3>{product.name}</h3>
        <p className="description">{product.description}</p>
        <p className="price">{product.price.toLocaleString()} ₽</p>
        <p className="stock">В наличии: {product.stock} шт.</p>
        <div className="buttons">
          <button className="edit" onClick={() => setEditing(true)}>Редактировать</button>
          <button className="delete" onClick={() => onDelete(product.id)}>Удалить</button>
        </div>
      </div>
    </div>
  );
}

export default ProductItem;