from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# Conexión a la base de datos
def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres'),
        port=os.getenv('DB_PORT', 5432),
        dbname=os.getenv('DB_NAME', 'itemsdb'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'pass123')
    )

# Health check
@app.route('/', methods=['GET'])
def health():
    return jsonify({
        "status": "OK",
        "message": "Flask + PostgreSQL CRUD Microservice running"
    })


# Obtener todos los items
@app.route('/items', methods=['GET'])
def get_items():
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM items")
        items = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(items)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Crear item
@app.route('/items', methods=['POST'])
def add_item():
    data = request.json

    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400

    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO items (name) VALUES (%s) RETURNING id",
            (data['name'],)
        )

        item_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "id": item_id,
            "name": data['name']
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Actualizar item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json

    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400

    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "UPDATE items SET name = %s WHERE id = %s RETURNING id, name",
            (data['name'], item_id)
        )

        updated = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if updated:
            return jsonify({
                "id": updated[0],
                "name": updated[1]
            })
        else:
            return jsonify({"error": "Item not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Eliminar item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM items WHERE id = %s RETURNING id",
            (item_id,)
        )

        deleted = cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        if deleted:
            return jsonify({
                "message": f"Item {item_id} deleted successfully"
            })
        else:
            return jsonify({"error": "Item not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Crear tabla si no existe
def init_db():
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """)

        conn.commit()
        cur.close()
        conn.close()

        print("Database initialized")

    except Exception as e:
        print("Database initialization error:", e)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)