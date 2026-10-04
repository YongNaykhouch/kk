from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
import uuid
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'change_this_to_a_strong_secret_key'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def get_db_connection():
    conn = sqlite3.connect('users.db', timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
@app.template_filter('format_currency')
def format_currency(value):
    try:
        return f"{int(value):,} ₫"
    except:
        return "0 ₫"

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Get all products with detailed specs - select all relevant columns
    all_products = conn.execute("""
        SELECT id, product_id, name, category, brand, price, image,
               cpu, display, ram, storage, gpu, battery, camera,
               chip, sensor, water_resistance,
               ports, wifi, cooling,
               capacity, type, cooling_tech, energy_rating, motor, technology, warranty, shelves,
               power, speed_levels, control_type, oscillation, timer, size, blade_type, filter,
               zones, burners, grates, safety, ignition
        FROM products
        ORDER BY id DESC
        LIMIT 8
    """).fetchall()

    # Get all products for category sections
    products = conn.execute("""
        SELECT id, product_id, name, category, brand, price, image,
               cpu, display, ram, storage, gpu, battery, camera,
               chip, sensor, water_resistance,
               ports, wifi, cooling,
               capacity, type, cooling_tech, energy_rating, motor, technology, warranty, shelves,
               power, speed_levels, control_type, oscillation, timer, size, blade_type, filter,
               zones, burners, grates, safety, ignition
        FROM products
        ORDER BY id DESC
    """).fetchall()
    conn.close()

    # Group products by category
    categories = defaultdict(list)
    for product in products:
        categories[product['category']].append(product)
    
    return render_template(
        'index.html',
        all_products=all_products,
        categories=categories
    )

# Helper function to get product specs based on category
def get_product_specs(product):
    """
    Returns a list of spec dictionaries for display
    Each dict has: {'icon': 'fa-icon-class', 'icon_type': 'cpu/ram/etc', 'value': 'spec value'}
    """
    specs = []
    category = product['category']
    
    # Phones (dienthoai)
    if category == 'dienthoai':
        if product['cpu']:
            specs.append({'icon': 'fa-microchip', 'icon_type': 'cpu', 'value': product['cpu']})
        if product['display']:
            specs.append({'icon': 'fa-desktop', 'icon_type': 'display', 'value': product['display']})
        if product['ram']:
            specs.append({'icon': 'fa-memory', 'icon_type': 'ram', 'value': product['ram']})
        if product['storage']:
            specs.append({'icon': 'fa-hard-drive', 'icon_type': 'storage', 'value': product['storage']})
        if product['camera']:
            specs.append({'icon': 'fa-camera', 'icon_type': 'camera', 'value': product['camera']})
        if product['battery']:
            specs.append({'icon': 'fa-battery-full', 'icon_type': 'battery', 'value': product['battery']})
    
    # Watches (dongho)
    elif category == 'dongho':
        if product['chip']:
            specs.append({'icon': 'fa-microchip', 'icon_type': 'chip', 'value': product['chip']})
        if product['display']:
            specs.append({'icon': 'fa-desktop', 'icon_type': 'display', 'value': product['display']})
        if product['sensor']:
            specs.append({'icon': 'fa-heartbeat', 'icon_type': 'sensor', 'value': product['sensor']})
        if product['battery']:
            specs.append({'icon': 'fa-battery-full', 'icon_type': 'battery', 'value': product['battery']})
        if product['water_resistance']:
            specs.append({'icon': 'fa-droplet', 'icon_type': 'water', 'value': product['water_resistance']})
        if product['storage']:
            specs.append({'icon': 'fa-hard-drive', 'icon_type': 'storage', 'value': product['storage']})
    
    # Laptops
    elif category == 'laptop':
        if product['cpu']:
            specs.append({'icon': 'fa-microchip', 'icon_type': 'cpu', 'value': product['cpu']})
        if product['display']:
            specs.append({'icon': 'fa-desktop', 'icon_type': 'display', 'value': product['display']})
        if product['ram']:
            specs.append({'icon': 'fa-memory', 'icon_type': 'ram', 'value': product['ram']})
        if product['storage']:
            specs.append({'icon': 'fa-hard-drive', 'icon_type': 'storage', 'value': product['storage']})
        if product['gpu']:
            specs.append({'icon': 'fa-display', 'icon_type': 'gpu', 'value': product['gpu']})
        if product['battery']:
            specs.append({'icon': 'fa-battery-full', 'icon_type': 'battery', 'value': product['battery']})
    
    # Desktops (maytinhbanpc)
    elif category == 'maytinhbanpc':
        if product['cpu']:
            specs.append({'icon': 'fa-microchip', 'icon_type': 'cpu', 'value': product['cpu']})
        if product['ram']:
            specs.append({'icon': 'fa-memory', 'icon_type': 'ram', 'value': product['ram']})
        if product['storage']:
            specs.append({'icon': 'fa-hard-drive', 'icon_type': 'storage', 'value': product['storage']})
        if product['gpu']:
            specs.append({'icon': 'fa-display', 'icon_type': 'gpu', 'value': product['gpu']})
        if product['ports']:
            specs.append({'icon': 'fa-plug', 'icon_type': 'ports', 'value': product['ports']})
        if product['wifi']:
            specs.append({'icon': 'fa-wifi', 'icon_type': 'wifi', 'value': product['wifi']})
    
    # Refrigerators (tulanh)
    elif category == 'tulanh':
        if product['capacity']:
            specs.append({'icon': 'fa-box', 'icon_type': 'capacity', 'value': product['capacity']})
        if product['type']:
            specs.append({'icon': 'fa-bolt', 'icon_type': 'type', 'value': product['type']})
        if product['cooling_tech']:
            specs.append({'icon': 'fa-snowflake', 'icon_type': 'cooling', 'value': product['cooling_tech']})
        if product['energy_rating']:
            specs.append({'icon': 'fa-star', 'icon_type': 'energy', 'value': product['energy_rating']})
        if product['warranty']:
            specs.append({'icon': 'fa-shield', 'icon_type': 'warranty', 'value': product['warranty']})
        if product['shelves']:
            specs.append({'icon': 'fa-table-cells', 'icon_type': 'shelves', 'value': product['shelves']})
    
    # Fans (quat)
    elif category == 'quat':
        if product['type']:
            specs.append({'icon': 'fa-fan', 'icon_type': 'type', 'value': product['type']})
        if product['power']:
            specs.append({'icon': 'fa-bolt', 'icon_type': 'power', 'value': product['power']})
        if product['speed_levels']:
            specs.append({'icon': 'fa-gauge-high', 'icon_type': 'speed', 'value': product['speed_levels']})
        if product['control_type']:
            specs.append({'icon': 'fa-mobile', 'icon_type': 'control', 'value': product['control_type']})
        if product['oscillation']:
            specs.append({'icon': 'fa-rotate', 'icon_type': 'oscillation', 'value': product['oscillation']})
        if product['timer']:
            specs.append({'icon': 'fa-clock', 'icon_type': 'timer', 'value': product['timer']})
    
    # Washing Machines (maygiatsay)
    elif category == 'maygiatsay':
        if product['capacity']:
            specs.append({'icon': 'fa-box', 'icon_type': 'capacity', 'value': product['capacity']})
        if product['type']:
            specs.append({'icon': 'fa-door-open', 'icon_type': 'type', 'value': product['type']})
        if product['motor']:
            specs.append({'icon': 'fa-gear', 'icon_type': 'motor', 'value': product['motor']})
        if product['technology']:
            specs.append({'icon': 'fa-sparkles', 'icon_type': 'technology', 'value': product['technology']})
        if product['energy_rating']:
            specs.append({'icon': 'fa-star', 'icon_type': 'energy', 'value': product['energy_rating']})
        if product['warranty']:
            specs.append({'icon': 'fa-shield', 'icon_type': 'warranty', 'value': product['warranty']})
    
    # Stoves (beptu)
    elif category == 'beptu':
        if product['type']:
            specs.append({'icon': 'fa-fire', 'icon_type': 'type', 'value': product['type']})
        if product['power']:
            specs.append({'icon': 'fa-bolt', 'icon_type': 'power', 'value': product['power']})
        if product['zones']:
            specs.append({'icon': 'fa-circle-dot', 'icon_type': 'zones', 'value': product['zones']})
        if product['burners']:
            specs.append({'icon': 'fa-fire-burner', 'icon_type': 'burners', 'value': product['burners']})
        if product['control_type']:
            specs.append({'icon': 'fa-hand-pointer', 'icon_type': 'control', 'value': product['control_type']})
        if product['safety']:
            specs.append({'icon': 'fa-shield', 'icon_type': 'safety', 'value': product['safety']})
    
    return specs

# Register the helper function as a Jinja2 filter
@app.template_filter('get_specs')
def get_specs_filter(product):
    return get_product_specs(dict(product))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip().lower()
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        dob = request.form.get('dob')
        address = request.form.get('address')
        avatar = request.files.get('avatar')

        # ❌ Reserved username
        if username.lower() == 'admin':
            flash('Username "admin" is reserved.', 'error')
            return render_template('register.html')

        # ❌ Gmail only
        if not email.endswith('@gmail.com'):
            flash('Chỉ cho phép đăng ký bằng Gmail!', 'error')
            return render_template('register.html')

        # ❌ Password mismatch
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp!', 'error')
            return render_template('register.html')

        # 🔐 Hash password
        hashed_password = hash_password(password)

        # 🖼 Avatar upload
        avatar_filename = None
        if avatar and allowed_file(avatar.filename):
            safe_name = secure_filename(avatar.filename)
            avatar_filename = f"{username}_{safe_name}"
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))

        conn = None
        try:
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO users 
                (username, email, phone, password, avatar, dob, address, role)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'user')
            """, (
                username,
                email,
                phone,
                hashed_password,
                avatar_filename,
                dob,
                address
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Tên đăng nhập hoặc Email đã tồn tại!', 'error')
            return render_template('register.html')
        except sqlite3.OperationalError:
            app.logger.exception('Database error during registration')
            flash('Cơ sở dữ liệu đang bận. Vui lòng thử lại sau!', 'error')
            return render_template('register.html')
        finally:
            if conn is not None:
                conn.close()

        flash('🎉 Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username'].strip().lower()
        password = hash_password(request.form['password'])

        conn = get_db_connection()
        user = conn.execute("""
            SELECT * FROM users
            WHERE (username = ? OR email = ?) AND password = ?
        """, (username_or_email, username_or_email, password)).fetchone()
        conn.close()

        if user:
            session.clear()
            session['user_id'] = user['id']
            session['customer_id'] = user['id']   # for cart JS
            session['username'] = user['username']
            session['role'] = user['role']

            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))

        flash('Sai tài khoản hoặc mật khẩu!', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất.', 'info')
    return redirect(url_for('login'))

@app.route('/products')
def products():
    """Customer product listing page - requires login"""
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để xem danh sách sản phẩm!', 'warning')
        return redirect(url_for('login'))
    
    if session.get('role') == 'admin':
        flash('Admin nên sử dụng trang quản trị.', 'info')
        return redirect(url_for('admin_products'))

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 12
    search = request.args.get('search', '').strip()

    conn = get_db_connection()
    
    base_query = """
        SELECT id, product_id, name, category, brand, price, stock, description, image,
               cpu, display, ram, storage, gpu, battery, camera,
               chip, sensor, water_resistance,
               ports, wifi, cooling,
               capacity, type, cooling_tech, energy_rating, motor, technology, warranty, shelves,
               power, speed_levels, control_type, oscillation, timer, size, blade_type, filter,
               zones, burners, grates, safety, ignition
        FROM products
    """

    if search:
        where_clause = "WHERE name LIKE ? OR brand LIKE ? OR category LIKE ?"
        params = (f'%{search}%', f'%{search}%', f'%{search}%')
        count_query = "SELECT COUNT(*) FROM products " + where_clause
        total = conn.execute(count_query, params).fetchone()[0]
        query = base_query + where_clause + " ORDER BY id DESC LIMIT ? OFFSET ?"
        params += (per_page, (page - 1) * per_page)
        products = conn.execute(query, params).fetchall()
    else:
        total = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        query = base_query + " ORDER BY id DESC LIMIT ? OFFSET ?"
        products = conn.execute(query, (per_page, (page - 1) * per_page)).fetchall()

    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template('products.html',
                           products=products,
                           page=page,
                           total_pages=total_pages,
                           search=search,
                           get_specs=get_product_specs)  # Pass helper directly if needed in template


@app.route('/admin_dashboard')
def admin_dashboard():
    """Admin main dashboard"""
    if session.get('role') != 'admin':
        flash('Chỉ admin mới có quyền truy cập!', 'danger')
        return redirect(url_for('index'))

    conn = get_db_connection()

    # Bảng users mặc định role = 'user' (không phải 'customer')
    total_users = conn.execute("SELECT COUNT(*) FROM users WHERE role != 'admin'").fetchone()[0]
    total_admins = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'").fetchone()[0]
    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    pending_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'").fetchone()[0]
    processing_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'processing'").fetchone()[0]
    completed_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'completed'").fetchone()[0]

    revenue_result = conn.execute("SELECT COALESCE(SUM(total_price), 0) FROM orders WHERE status = 'completed'").fetchone()
    total_revenue = revenue_result[0]

    # Recent users
    recent_users = conn.execute("""
        SELECT id, username, email, role
        FROM users
        ORDER BY id DESC LIMIT 10
    """).fetchall()

    # Recent orders
    recent_orders = conn.execute("""
        SELECT o.id,  o.total_price, o.status, o.created_at, u.username
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.id DESC LIMIT 10
    """).fetchall()

    conn.close()

    return render_template('admin_dashboard.html',
                           page='dashboard',
                           total_users=total_users,
                           total_admins=total_admins,
                           total_products=total_products,
                           pending_orders=pending_orders,
                           processing_orders=processing_orders,
                           completed_orders=completed_orders,
                           total_revenue=total_revenue,
                           recent_users=recent_users,
                           recent_orders=recent_orders)


@app.route('/admin/products')
def admin_products():
    """Admin product management page"""
    if session.get('role') != 'admin':
        flash('Chỉ admin mới có quyền truy cập!', 'danger')
        return redirect(url_for('index'))

    # Search & Pagination
    # Hiển thị TẤT CẢ sản phẩm trên một trang (không giới hạn 15 như trước)
    page = 1
    per_page = 100000
    search = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    conn = get_db_connection()

    where_conditions = []
    params = []

    if search:
        where_conditions.append("(name LIKE ? OR brand LIKE ? OR product_id LIKE ?)")
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])

    if category_filter:
        where_conditions.append("category = ?")
        params.append(category_filter)

    where_clause = " AND ".join(where_conditions)
    if where_clause:
        where_clause = "WHERE " + where_clause

    # Count total
    count_query = f"SELECT COUNT(*) FROM products {where_clause}"
    total = conn.execute(count_query, params).fetchone()[0]

    # Fetch products
    query = f"""
        SELECT id, product_id, name, category, brand, price, stock, description, image, created_at
        FROM products
        {where_clause}
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """
    params.extend([per_page, (page - 1) * per_page])
    products = conn.execute(query, params).fetchall()

    # Get categories for filter dropdown
    categories = conn.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    categories = [row['category'] for row in categories]

    # Stats for sidebar/cards
    total_users = conn.execute("SELECT COUNT(*) FROM users WHERE role != 'admin'").fetchone()[0]
    pending_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'").fetchone()[0]
    total_revenue = conn.execute("SELECT COALESCE(SUM(total_price), 0) FROM orders WHERE status = 'completed'").fetchone()[0]

    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template('admin_dashboard.html',
                           page='products',
                           products=products,
                           total_products=total,
                           page_num=page,
                           total_pages=total_pages,
                           search=search,
                           category_filter=category_filter,
                           categories=categories,
                           total_users=total_users,
                           pending_orders=pending_orders,
                           total_revenue=total_revenue)

@app.route('/admin/add_product')
def admin_add_product():
    """Main menu: Show category selection buttons"""
    if session.get('role') != 'admin':
        flash('Admin access only!', 'error')
        return redirect(url_for('index'))

    return render_template('add_product.html')  # The page with big category buttons


@app.route('/admin/add_product/<category>', methods=['GET', 'POST'])
def admin_add_product_category(category):
    """Add product for a specific category with tailored fields"""
    if session.get('role') != 'admin':
        flash('Admin access only!', 'error')
        return redirect(url_for('index'))

    # Validate category
    valid_categories = {
        'dienthoai', 'dongho', 'laptop', 'maytinhbanpc',
        'tulanh', 'quat', 'maygiatsay', 'beptu'
    }
    if category not in valid_categories:
        flash('Danh mục không hợp lệ!', 'error')
        return redirect(url_for('admin_add_product'))

    # Human-readable names and icons for template
    category_info = {
        'dienthoai': ('Điện Thoại', 'fa-mobile-alt'),
        'dongho': ('Đồng Hồ Thông Minh', 'fa-watch'),
        'laptop': ('Laptop', 'fa-laptop'),
        'maytinhbanpc': ('Máy Tính Bàn / PC', 'fa-desktop'),
        'tulanh': ('Tủ Lạnh', 'fa-snowflake'),
        'quat': ('Quạt', 'fa-fan'),
        'maygiatsay': ('Máy Giặt & Sấy', 'fa-tshirt'),
        'beptu': ('Bếp Từ', 'fa-fire-burner'),
    }
    category_name, icon_class = category_info[category]

    if request.method == 'POST':
        # Common fields
        name = request.form.get('name')
        brand = request.form.get('brand')
        price_str = request.form.get('price')
        stock_str = request.form.get('stock')
        description = request.form.get('description')

        # Validation
        if not name or not price_str:
            flash('Tên sản phẩm và giá là bắt buộc!', 'error')
            return redirect(request.url)

        try:
            price = float(price_str)
            if price < 0:
                raise ValueError
        except ValueError:
            flash('Giá phải là số dương hợp lệ!', 'error')
            return redirect(request.url)

        # Stock (số lượng) - mặc định 0 nếu bỏ trống
        try:
            stock = int(stock_str) if stock_str else 0
            if stock < 0:
                stock = 0
        except (TypeError, ValueError):
            stock = 0

        # Image upload
        if 'image' not in request.files:
            flash('Vui lòng chọn hình ảnh!', 'error')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('Chưa chọn file ảnh!', 'error')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Định dạng ảnh không hợp lệ! Chỉ chấp nhận: PNG, JPG, JPEG, GIF.', 'error')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Generate unique product_id (visible code)
        product_id = str(uuid.uuid4())[:8].upper()

        # Category-specific fields (only get if submitted)
        spec_fields = [
            'cpu', 'display', 'ram', 'storage', 'gpu', 'battery', 'camera',
            'chip', 'sensor', 'water_resistance',
            'ports', 'wifi', 'cooling',
            'capacity', 'type', 'cooling_tech', 'energy_rating', 'motor',
            'technology', 'warranty', 'shelves',
            'power', 'speed_levels', 'control_type', 'oscillation', 'timer',
            'size', 'blade_type', 'filter',
            'zones', 'burners', 'grates', 'safety', 'ignition'
        ]

        specs = {field: request.form.get(field) or None for field in spec_fields}

        try:
            conn = get_db_connection()

            # Full INSERT with all possible columns
            conn.execute('''
                INSERT INTO products (
                    product_id, name, category, brand, price, stock, description, image,
                    cpu, display, ram, storage, gpu, battery, camera,
                    chip, sensor, water_resistance,
                    ports, wifi, cooling,
                    capacity, type, cooling_tech, energy_rating, motor, technology, warranty, shelves,
                    power, speed_levels, control_type, oscillation, timer, size, blade_type, filter,
                    zones, burners, grates, safety, ignition
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?
                )

            ''', (
                product_id, name, category, brand, price, stock, description, unique_filename,
                specs['cpu'], specs['display'], specs['ram'], specs['storage'], specs['gpu'], specs['battery'], specs['camera'],
                specs['chip'], specs['sensor'], specs['water_resistance'],
                specs['ports'], specs['wifi'], specs['cooling'],
                specs['capacity'], specs['type'], specs['cooling_tech'], specs['energy_rating'], specs['motor'],
                specs['technology'], specs['warranty'], specs['shelves'],
                specs['power'], specs['speed_levels'], specs['control_type'], specs['oscillation'], specs['timer'],
                specs['size'], specs['blade_type'], specs['filter'],
                specs['zones'], specs['burners'], specs['grates'], specs['safety'], specs['ignition']
            ))

            conn.commit()
            conn.close()

            flash(f'Thêm sản phẩm "{name}" thành công!', 'success')
            return redirect(url_for('admin_products'))

        except Exception as e:
            # Log error if needed: print(e)
            flash('Đã xảy ra lỗi khi thêm sản phẩm. Vui lòng thử lại.', 'error')
            if os.path.exists(filepath):
                os.remove(filepath)
            return redirect(request.url)

    # GET: Show the form
    return render_template('add_product_form.html',
                           category=category,
                           category_name=category_name,
                           icon=icon_class)

@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    if session.get('role') != 'admin':
        flash('Admin access only!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()

    # Fetch product using dictionary access
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    if product is None:
        flash('Sản phẩm không tồn tại!', 'error')
        conn.close()
        return redirect(url_for('admin_products'))

    # URL quay về form khi validate thất bại.
    # KHÔNG dùng request.url vì route nhận <int:product_id> nhưng product['id'] là
    # khoá chính (int) - dùng url_for cho chắc chắn đúng và không bị 404.
    form_url = url_for('admin_edit_product', product_id=product['id'])

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        brand = request.form.get('brand')
        price_str = request.form.get('price')
        stock_str = request.form.get('stock')
        description = request.form.get('description')

        if not all([name, category, brand, price_str]):
            flash('Vui lòng điền đầy đủ thông tin!', 'error')
            conn.close()
            return redirect(form_url)

        try:
            price = float(price_str)
            if price < 0:
                raise ValueError
        except ValueError:
            flash('Giá phải là số dương hợp lệ!', 'error')
            conn.close()
            return redirect(form_url)

        # Stock (số lượng) - mặc định 0 nếu bỏ trống
        try:
            stock = int(stock_str) if stock_str else 0
            if stock < 0:
                stock = 0
        except (TypeError, ValueError):
            stock = 0

        # Handle image update (optional)
        image_filename = product['image']  # ← Fixed: use ['image']
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                if not allowed_file(file.filename):
                    flash('Định dạng file không hợp lệ! Chỉ chấp nhận PNG, JPG, JPEG, GIF.', 'error')
                    conn.close()
                    return redirect(form_url)

                # Delete old image
                if image_filename:
                    old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)

                # Save new image
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                image_filename = unique_filename

        # Update database
        conn.execute('''
            UPDATE products
            SET name = ?, category = ?, brand = ?, price = ?, stock = ?, description = ?, image = ?
            WHERE id = ?
        ''', (name, category, brand, price, stock, description, image_filename, product['id']))
        conn.commit()
        conn.close()

        flash('Cập nhật sản phẩm thành công!', 'success')
        return redirect(url_for('admin_products'))

    # GET request: show form
    conn.close()
    return render_template('edit_product.html', product=product)  # product is sqlite3.Row → use ['key'] in template too!

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
def admin_delete_product(product_id):
    if session.get('role') != 'admin':
        flash('Admin access only!', 'error')
        return redirect(url_for('index'))

    # 1. Lấy image
    with get_db_connection() as conn:
        product = conn.execute(
            'SELECT image FROM products WHERE id = ?',
            (product_id,)
        ).fetchone()

    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('admin_products'))

    image_filename = product['image']

    # 2. Xóa file ảnh
    if image_filename:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    # 3. Xóa order_items trước, rồi mới xóa product
    # LƯU Ý: `with get_db_connection() as conn` chỉ đóng connection, KHÔNG tự commit.
    # Thiếu conn.commit() thì lệnh DELETE bị rollback khi đóng -> sản phẩm không bị xóa.
    conn = get_db_connection()
    try:
        conn.execute(
            'DELETE FROM order_items WHERE product_id = ?',
            (product_id,)
        )
        conn.execute(
            'DELETE FROM products WHERE id = ?',
            (product_id,)
        )
        conn.commit()
    finally:
        conn.close()

    flash('Xóa sản phẩm thành công!', 'success')
    return redirect(url_for('admin_products'))




@app.template_filter('strftime')
def _jinja2_filter_strftime(date_str, fmt):
    if not date_str:
        return ""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date.strftime(fmt)
    except:
        return date_str  # nếu lỗi thì trả về nguyên bản




@app.route('/admin/orders')
def admin_orders():
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()

    # Lấy tham số filter từ URL: ?status=pending
    status_filter = request.args.get('status')  # None hoặc 'pending', 'processing',...

    # ================== THỐNG KÊ SỐ LƯỢNG THEO TRẠNG THÁI ==================
    counts = {
        'all': conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0],
        'pending': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'").fetchone()[0],
        'processing': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'processing'").fetchone()[0],
        'shipped': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'shipped'").fetchone()[0],
        'completed': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'completed'").fetchone()[0],
        'cancelled': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'cancelled'").fetchone()[0],
    }

    # ================== LẤY DANH SÁCH ĐƠN HÀNG ==================
    if status_filter and status_filter in ['pending', 'processing', 'shipped', 'completed', 'cancelled']:
        orders_raw = conn.execute("""
            SELECT 
                o.id,
                o.order_id,
                o.total_price,
                o.status,
                o.address,
                o.phone,
                o.created_at,
                u.username,
                u.email
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.status = ?
            ORDER BY o.created_at DESC
        """, (status_filter,)).fetchall()
    else:
        # Không filter → lấy tất cả
        orders_raw = conn.execute("""
            SELECT 
                o.id,
                o.order_id,
                o.total_price,
                o.status,
                o.address,
                o.phone,
                o.created_at,
                u.username,
                u.email
            FROM orders o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.created_at DESC
        """).fetchall()

    # ================== XỬ LÝ created_at → datetime object (giữ nguyên fix tốt của mày) ==================
    orders = []
    for order in orders_raw:
        order_dict = dict(order)
        if order_dict['created_at']:
            created_at_str = order_dict['created_at']
            try:
                if '.' in created_at_str:
                    order_dict['created_at'] = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    order_dict['created_at'] = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # Fallback an toàn: bỏ phần microsecond nếu lỗi
                order_dict['created_at'] = datetime.strptime(created_at_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
        orders.append(order_dict)

    # ================== THỐNG KÊ KHÁC CHO DASHBOARD ==================
    total_revenue = conn.execute(
        "SELECT COALESCE(SUM(total_price), 0) FROM orders WHERE status = 'completed'"
    ).fetchone()[0]

    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]

    conn.close()

    return render_template(
        'admin_dashboard.html',  # hoặc 'admin/orders.html' nếu tách riêng
        page='orders',
        orders=orders,
        counts=counts,              # ← Quan trọng: truyền counts để hiển thị badge
        status=status_filter,       # ← Để highlight nút đang chọn
        pending_count=counts['pending'],
        total_revenue=total_revenue,
        total_users=total_users,
        total_products=total_products
    )


# =====================================================================
# TRANG "ĐƠN HÀNG" (tra cứu / lịch sử) - KHÁC với "Quản Lý Đơn Hàng"
# - /admin/orders      : XỬ LÝ đơn (xác nhận, đổi trạng thái, xóa)
# - /admin/order-list  : TRA CỨU hóa đơn (tìm kiếm, lọc ngày, in/xem chi tiết)
# =====================================================================
@app.route('/admin/order-list')
def admin_order_list():
    """Trang tra cứu hóa đơn (chỉ đọc, không sửa/xóa)."""
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    # ================== THAM SỐ TÌM KIẾM / SẮP XẾP / PHÂN TRANG ==================
    keyword = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    sort = request.args.get('sort', 'newest').strip()
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1
    per_page = 15

    VALID_STATUS = ['pending', 'processing', 'shipped', 'completed', 'cancelled']
    if status_filter not in VALID_STATUS:
        status_filter = ''

    # Chỉ cho phép các kiểu sắp xếp an toàn (tránh SQL injection)
    SORT_OPTIONS = {
        'newest': 'o.created_at DESC',
        'oldest': 'o.created_at ASC',
        'price_desc': 'o.total_price DESC',
        'price_asc': 'o.total_price ASC',
    }
    order_by = SORT_OPTIONS.get(sort, SORT_OPTIONS['newest'])

    conn = get_db_connection()

    # ================== ĐIỀU KIỆN WHERE ==================
    where_conditions = []
    params = []

    if keyword:
        where_conditions.append(
            "(o.order_id LIKE ? OR u.username LIKE ? OR u.email LIKE ? OR o.phone LIKE ?)"
        )
        like = f'%{keyword}%'
        params.extend([like, like, like, like])

    if status_filter:
        where_conditions.append("o.status = ?")
        params.append(status_filter)

    if date_from:
        where_conditions.append("DATE(o.created_at) >= DATE(?)")
        params.append(date_from)

    if date_to:
        where_conditions.append("DATE(o.created_at) <= DATE(?)")
        params.append(date_to)

    where_clause = ("WHERE " + " AND ".join(where_conditions)) if where_conditions else ""

    # ================== TỔNG SỐ KẾT QUẢ & TỔNG TIỀN ==================
    totals = conn.execute(f"""
        SELECT COUNT(*) AS cnt,
               COALESCE(SUM(o.total_price), 0) AS amount
        FROM orders o
        JOIN users u ON o.user_id = u.id
        {where_clause}
    """, params).fetchone()
    total = totals['cnt']
    filtered_amount = totals['amount']

    # ================== LẤY DỮ LIỆU TRANG HIỆN TẠI ==================
    orders_raw = conn.execute(f"""
        SELECT
            o.id,
            o.order_id,
            o.total_price,
            o.status,
            o.address,
            o.phone,
            o.created_at,
            u.username,
            u.email,
            (SELECT COALESCE(SUM(oi.quantity), 0)
             FROM order_items oi
             WHERE oi.order_id = o.order_id) AS item_count
        FROM orders o
        JOIN users u ON o.user_id = u.id
        {where_clause}
        ORDER BY {order_by}
        LIMIT ? OFFSET ?
    """, params + [per_page, (page - 1) * per_page]).fetchall()

    # ================== created_at (string) → datetime ==================
    orders = []
    for order in orders_raw:
        order_dict = dict(order)
        if order_dict['created_at']:
            created_at_str = order_dict['created_at']
            try:
                if '.' in created_at_str:
                    order_dict['created_at'] = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    order_dict['created_at'] = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                order_dict['created_at'] = datetime.strptime(created_at_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
        orders.append(order_dict)

    # ================== THỐNG KÊ THEO TRẠNG THÁI (toàn hệ thống) ==================
    summary = {
        'total': conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0],
        'pending': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'").fetchone()[0],
        'processing': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'processing'").fetchone()[0],
        'shipped': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'shipped'").fetchone()[0],
        'completed': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'completed'").fetchone()[0],
        'cancelled': conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'cancelled'").fetchone()[0],
    }

    total_revenue = conn.execute(
        "SELECT COALESCE(SUM(total_price), 0) FROM orders WHERE status = 'completed'"
    ).fetchone()[0]
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]

    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        'admin_dashboard.html',
        page='order_list',
        orders=orders,
        summary=summary,
        keyword=keyword,
        status=status_filter,
        date_from=date_from,
        date_to=date_to,
        sort=sort,
        page_num=page,
        per_page=per_page,
        total_pages=total_pages,
        total_results=total,
        filtered_amount=filtered_amount,
        pending_count=summary['pending'],
        total_revenue=total_revenue,
        total_users=total_users,
        total_products=total_products
    )


@app.route('/admin/order_detail/<string:order_id>')
def admin_order_detail(order_id):
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()

    # Get order info
    order = conn.execute("""
        SELECT 
            o.*,
            u.username,
            u.email,
            u.phone AS user_phone,
            u.address AS user_address
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.order_id = ?
    """, (order_id,)).fetchone()

    if not order:
        flash('Đơn hàng không tồn tại!', 'error')
        conn.close()
        return redirect(url_for('admin_orders'))

    # Get order items
    items = conn.execute("""
        SELECT 
            product_name,
            price,
            quantity,
            (price * quantity) AS subtotal
        FROM order_items
        WHERE order_id = ?
    """, (order_id,)).fetchall()

    conn.close()

    return render_template('admin_order_detail.html',
                          order=order,
                          items=items)

@app.route('/admin/order/edit/<string:order_id>', methods=['GET', 'POST'])
def admin_edit_order(order_id):
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()

    if request.method == 'POST':
        new_status = request.form.get('status')

        conn.execute("""
            UPDATE orders
            SET status = ?
            WHERE order_id = ?
        """, (new_status, order_id))

        conn.commit()
        conn.close()

        flash('Cập nhật trạng thái đơn hàng thành công!', 'success')
        return redirect(url_for('admin_orders'))

    order = conn.execute("""
        SELECT order_id, status
        FROM orders
        WHERE order_id = ?
    """, (order_id,)).fetchone()

    conn.close()

    if not order:
        flash('Đơn hàng không tồn tại!', 'error')
        return redirect(url_for('admin_orders'))

    return render_template(
        'admin_edit_order.html',
        order=order
    )
@app.route('/admin/order/delete/<string:order_id>', methods=['POST'])
def admin_delete_order(order_id):
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()

    conn.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
    conn.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    conn.commit()
    conn.close()

    flash('Đã xóa đơn hàng thành công!', 'success')
    return redirect(url_for('admin_orders'))



from datetime import datetime, timedelta

@app.route('/admin/reports')
def admin_reports():
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()

    # ===== THỐNG KÊ CƠ BẢN =====
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]

    total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    pending_count = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'").fetchone()[0]

    total_revenue = conn.execute("""
        SELECT COALESCE(SUM(total_price), 0)
        FROM orders WHERE status = 'completed'
    """).fetchone()[0]

    products_sold = conn.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status = 'completed'
    """).fetchone()[0]

    # ===== TRẠNG THÁI ĐƠN HÀNG (CHO DOUGHNUT CHART) =====
    order_status_stats = conn.execute("""
        SELECT 
            status,
            COUNT(*) as count,
            CASE status
                WHEN 'pending' THEN 'Chờ xác nhận'
                WHEN 'processing' THEN 'Đang xử lý'
                WHEN 'shipped' THEN 'Đang giao'
                WHEN 'completed' THEN 'Đã giao'
                WHEN 'cancelled' THEN 'Đã hủy'
                ELSE status
            END as label
        FROM orders
        GROUP BY status
    """).fetchall()

    status_labels = [row['label'] for row in order_status_stats]
    status_counts = [row['count'] for row in order_status_stats]

    # Màu sắc đẹp cho chart (tương thích dark/light mode)
    status_colors = ['#0c06cd', '#0dcaf0', '#0d6efd', '#198754', '#dc3545']

    # ===== DOANH THU 7 NGÀY GẦN NHẤT =====
    from datetime import datetime, timedelta
    today = datetime.now().date()
    start_date = today - timedelta(days=6)

    revenue_rows = conn.execute("""
        SELECT 
            DATE(created_at) as day,
            COALESCE(SUM(total_price), 0) as revenue
        FROM orders
        WHERE status = 'completed'
          AND DATE(created_at) >= ?
        GROUP BY DATE(created_at)
        ORDER BY day
    """, (start_date.strftime('%Y-%m-%d'),)).fetchall()

    # Tạo đầy đủ 7 ngày (kể cả ngày chưa có doanh thu = 0)
    revenue_labels = []
    revenue_data = []
    for i in range(7):
        day = (start_date + timedelta(days=i)).strftime('%d/%m')
        revenue_labels.append(day)
        
        found = next((row['revenue'] for row in revenue_rows if row['day'] == (start_date + timedelta(days=i)).strftime('%Y-%m-%d')), 0)
        revenue_data.append(float(found))

    # ===== TOP 5 SẢN PHẨM BÁN CHẠY =====
    top_products = conn.execute("""
        SELECT 
            p.name,
            COALESCE(SUM(oi.quantity), 0) as quantity,
            COALESCE(SUM(oi.price * oi.quantity), 0) as revenue
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.status = 'completed'
        GROUP BY p.id, p.name
        ORDER BY quantity DESC
        LIMIT 5
    """).fetchall()

    # ===== TOP 5 KHÁCH HÀNG THÂN THIẾT =====
    top_customers = conn.execute("""
        SELECT 
            u.username as name,
            COUNT(o.order_id) as orders,
            COALESCE(SUM(o.total_price), 0) as total
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.status = 'completed'
        GROUP BY u.id, u.username
        ORDER BY total DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return render_template(
        'admin_dashboard.html',
        page='reports',
        # Stats
        total_users=total_users,
        total_products=total_products,
        total_orders=total_orders,
        pending_count=pending_count,
        total_revenue=total_revenue,
        products_sold=products_sold,
        # Charts
        status_labels=status_labels,
        status_counts=status_counts,
        status_colors=status_colors,
        revenue_labels=revenue_labels,
        revenue_data=revenue_data,
        # Tables
        top_products=top_products,
        top_customers=top_customers
    )

# ================== ĐẢM BẢO FORMAT_CURRENCY CÓ SẴN TRONG MỌI TEMPLATE ==================
@app.context_processor
def inject_format_currency():
    def format_currency(value):
        try:
            return f"{int(float(value)):,} ₫"
        except (ValueError, TypeError):
            return "0 ₫"
    return dict(format_currency=format_currency)


# === ADMIN: QUẢN LÝ KHÁCH HÀNG ===
@app.route('/admin/customers')
def admin_customers():
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()

    # ===== USERS =====
    customers = conn.execute("""
        SELECT 
            id,
            username AS name,
            email,
            phone,
            address,
            avatar
        FROM users
        ORDER BY id DESC
    """).fetchall()

    # ===== ENRICH CUSTOMERS =====
    enriched_customers = []
    for customer in customers:
        order_stats = conn.execute("""
            SELECT 
                COUNT(*) AS order_count,
                COALESCE(SUM(total_price), 0) AS total_spent
            FROM orders
            WHERE user_id = ? AND status = 'completed'
        """, (customer['id'],)).fetchone()

        enriched_customers.append({
            'id': customer['id'],
            'name': customer['name'],
            'email': customer['email'],
            'phone': customer['phone'] or 'Chưa cập nhật',
            'address': customer['address'] or 'Chưa cập nhật',
            'avatar': customer['avatar'],
            'order_count': order_stats['order_count'],
            'total_spent': order_stats['total_spent']
        })

    # ===== STATS FOR CARDS =====
    total_users = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    total_products = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    pending_count = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE status = 'pending'"
    ).fetchone()[0]

    total_revenue = conn.execute("""
        SELECT COALESCE(SUM(total_price), 0)
        FROM orders
        WHERE status = 'completed'
    """).fetchone()[0]

    conn.close()

    return render_template(
        'admin_dashboard.html',
        page='customers',
        customers=enriched_customers,
        total_users=total_users,
        total_products=total_products,
        pending_count=pending_count,
        total_revenue=total_revenue
    )

@app.route('/admin/customer/<int:customer_id>')
def admin_view_customer(customer_id):
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()
    
    customer = conn.execute("""
        SELECT id, username, email, phone, address, avatar, dob
        FROM users 
        WHERE id = ? AND role = 'user'
    """, (customer_id,)).fetchone()

    if not customer:
        flash('Khách hàng không tồn tại!', 'error')
        conn.close()
        return redirect(url_for('admin_customers'))

    # Thống kê đơn hàng
    stats = conn.execute("""
        SELECT 
            COUNT(*) AS order_count,
            COALESCE(SUM(total_price), 0) AS total_spent
        FROM orders 
        WHERE user_id = ? AND status = 'completed'
    """, (customer_id,)).fetchone()

    # 5 đơn hàng gần nhất + FIX created_at
    recent_orders_raw = conn.execute("""
        SELECT order_id, total_price, status, created_at
        FROM orders 
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 5
    """, (customer_id,)).fetchall()

    # CHUYỂN STRING → DATETIME (giống admin_orders)
    recent_orders = []
    for order in recent_orders_raw:
        order_dict = dict(order)
        if order_dict['created_at']:
            created_at_str = order_dict['created_at']
            try:
                if '.' in created_at_str:
                    order_dict['created_at'] = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    order_dict['created_at'] = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                order_dict['created_at'] = datetime.strptime(created_at_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
        recent_orders.append(order_dict)

    # Stats cho dashboard cards
    total_users = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'user'").fetchone()[0]
    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    pending_count = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'").fetchone()[0]
    total_revenue = conn.execute("SELECT COALESCE(SUM(total_price), 0) FROM orders WHERE status = 'completed'").fetchone()[0]

    conn.close()

    return render_template('admin_customer_detail.html',
                          page='customer_detail',  # Để hiển thị stats cards nếu cần
                          customer=customer,
                          stats=stats,
                          recent_orders=recent_orders,
                          total_users=total_users,
                          total_products=total_products,
                          pending_count=pending_count,
                          total_revenue=total_revenue)

@app.route('/admin/customer/edit/<int:customer_id>', methods=['GET', 'POST'])
def admin_edit_customer(customer_id):
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()
    customer = conn.execute("SELECT * FROM users WHERE id = ? AND role = 'user'", (customer_id,)).fetchone()

    if not customer:
        flash('Khách hàng không tồn tại!', 'error')
        conn.close()
        return redirect(url_for('admin_customers'))

    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip().lower()
        phone = request.form.get('phone')
        address = request.form.get('address')
        dob = request.form.get('dob')

        if username.lower() == 'admin':
            flash('Không được dùng tên "admin"!', 'error')
            conn.close()
            return redirect(request.url)

        # Xử lý avatar
        avatar_filename = customer['avatar']
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file.filename != '':
                if not allowed_file(file.filename):
                    flash('File không hợp lệ! Chỉ chấp nhận PNG, JPG, JPEG, GIF.', 'error')
                    conn.close()
                    return redirect(request.url)

                # Xóa avatar cũ
                if avatar_filename:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)

                # Lưu avatar mới
                safe_name = secure_filename(file.filename)
                new_filename = f"user_{customer_id}_{uuid.uuid4().hex}_{safe_name}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                avatar_filename = new_filename

        try:
            conn.execute("""
                UPDATE users 
                SET username = ?, email = ?, phone = ?, address = ?, dob = ?, avatar = ?
                WHERE id = ?
            """, (username, email, phone, address, dob, avatar_filename, customer_id))
            conn.commit()
            flash('Cập nhật thông tin khách hàng thành công!', 'success')
        except sqlite3.IntegrityError:
            flash('Email hoặc tên đăng nhập đã tồn tại!', 'error')

        conn.close()
        return redirect(url_for('admin_customers'))

    conn.close()
    return render_template('admin_edit_customer.html', customer=customer)


@app.route('/admin/customer/delete/<int:customer_id>', methods=['POST'])
def admin_delete_customer(customer_id):
    if session.get('role') != 'admin':
        flash('Chỉ quản trị viên mới được truy cập!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()

    customer = conn.execute("SELECT avatar FROM users WHERE id = ? AND role = 'user'", (customer_id,)).fetchone()
    if not customer:
        flash('Khách hàng không tồn tại!', 'error')
        conn.close()
        return redirect(url_for('admin_customers'))

    # Xóa avatar
    if customer['avatar']:
        path = os.path.join(app.config['UPLOAD_FOLDER'], customer['avatar'])
        if os.path.exists(path):
            os.remove(path)

    # Xóa dữ liệu liên quan (an toàn với foreign key)
    conn.execute("DELETE FROM order_items WHERE order_id IN (SELECT order_id FROM orders WHERE user_id = ?)", (customer_id,))
    conn.execute("DELETE FROM orders WHERE user_id = ?", (customer_id,))
    conn.execute("DELETE FROM users WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()

    flash('Đã xóa khách hàng và toàn bộ đơn hàng liên quan!', 'success')
    return redirect(url_for('admin_customers'))

@app.route('/cart', strict_slashes=False, methods=['GET', 'POST'])
def view_cart():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để xem giỏ hàng!', 'warning')
        return redirect(url_for('login'))

    if session.get('role') == 'admin':
        flash('Admin không thể truy cập giỏ hàng khách hàng!', 'danger')
        return redirect(url_for('admin_dashboard'))

    cart = session.get('cart', {})
    cart_items = list(cart.values())
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    conn = get_db_connection()

    # Lấy thông tin user
    user = conn.execute("SELECT username, email, phone, address FROM users WHERE id = ?", 
                        (session['user_id'],)).fetchone()

    # Lấy lịch sử đơn hàng
    orders = conn.execute("""
        SELECT o.order_id, o.total_price, o.status, o.address, o.phone, o.created_at,
               COUNT(oi.id) AS item_count
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.user_id = ?
        GROUP BY o.order_id
        ORDER BY o.created_at DESC
        LIMIT 20
    """, (session['user_id'],)).fetchall()
    conn.close()

    user_info = {
        'username': user['username'] if user else 'Khách hàng',
        'email': user['email'] if user else '',
        'phone': user['phone'] or '',
        'address': user['address'] or ''
    }

    if request.method == 'POST':
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        note = request.form.get('note', '').strip()  # Có thể để trống

        if not address or not phone:
            flash('Vui lòng nhập đầy đủ địa chỉ và số điện thoại!', 'danger')
            return redirect(url_for('view_cart'))

        if not cart_items:
            flash('Giỏ hàng của bạn đang trống!', 'warning')
            return redirect(url_for('view_cart'))

        try:
            conn = get_db_connection()
            order_id = str(uuid.uuid4())[:12].upper()
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Định dạng chuỗi an toàn

            # === KIỂM TRA VÀ CHÈN AN TOÀN ===
            cursor = conn.cursor()
            
            # Kiểm tra xem cột note có tồn tại không
            cursor.execute("PRAGMA table_info(orders)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'note' in columns and 'created_at' in columns:
                # Có đủ cột → chèn đầy đủ
                conn.execute("""
                    INSERT INTO orders 
                    (order_id, user_id, total_price, status, address, phone, note, created_at)
                    VALUES (?, ?, ?, 'pending', ?, ?, ?, ?)
                """, (order_id, session['user_id'], total, address, phone, note, created_at))
            elif 'created_at' in columns:
                # Chỉ có created_at, không có note
                conn.execute("""
                    INSERT INTO orders 
                    (order_id, user_id, total_price, status, address, phone, created_at)
                    VALUES (?, ?, ?, 'pending', ?, ?, ?)
                """, (order_id, session['user_id'], total, address, phone, created_at))
            else:
                # Chỉ có cấu trúc cơ bản (không có note và created_at)
                conn.execute("""
                    INSERT INTO orders 
                    (order_id, user_id, total_price, status, address, phone)
                    VALUES (?, ?, ?, 'pending', ?, ?)
                """, (order_id, session['user_id'], total, address, phone))

            # Thêm các sản phẩm vào order_items
            for item in cart_items:
                conn.execute("""
                    INSERT INTO order_items 
                    (order_id, product_id, product_name, price, quantity)
                    VALUES (?, ?, ?, ?, ?)
                """, (order_id, item['id'], item['name'], item['price'], item['quantity']))

            conn.commit()
            conn.close()

            # Cập nhật thông tin giao hàng cho user
            try:
                conn = get_db_connection()
                conn.execute("UPDATE users SET phone = ?, address = ? WHERE id = ?",
                             (phone, address, session['user_id']))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Lỗi cập nhật thông tin user: {e}")

            # Xóa giỏ hàng
            session.pop('cart', None)
            session.modified = True

            flash(f'Đặt hàng thành công! Mã đơn: #{order_id}', 'success')
            return redirect(url_for('view_cart'))

        except Exception as e:
            print(f"[LỖI ĐẶT HÀNG] {e}")  # In ra console để bạn xem lỗi thật
            flash('Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại sau!', 'danger')
            return redirect(url_for('view_cart'))

    return render_template('cart.html',
                           cart=cart_items,
                           total=total,
                           user=user_info,
                           orders=orders)
@app.route('/add_to_cart/<int:product_id>')
@app.route('/add_to_cart/<int:product_id>/<int:quantity>')
def add_to_cart(product_id, quantity=1):
    if 'user_id' not in session or session.get('role') == 'admin':
        flash('Chỉ khách hàng mới được thêm vào giỏ!', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()

    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('index'))

    cart = session.get('cart', {})

    key = str(product_id)
    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'image': product['image'],
            'quantity': quantity
        }

    session['cart'] = cart
    flash(f'Đã thêm "{product["name"]}" vào giỏ hàng!', 'success')
    return redirect(url_for('index'))

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập!', 'error')
        return redirect(url_for('login'))

    quantity = request.form.get('quantity', type=int)

    if quantity is None or quantity < 1:
        flash('Số lượng không hợp lệ!', 'error')
    else:
        cart = session.get('cart', {})
        key = str(product_id)
        if key in cart:
            if quantity == 0:
                del cart[key]
                flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'info')
            else:
                cart[key]['quantity'] = quantity
                flash('Cập nhật số lượng thành công!', 'success')
            session['cart'] = cart
        else:
            flash('Sản phẩm không tồn tại trong giỏ!', 'error')

    return redirect(url_for('view_cart'))


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để thao tác giỏ hàng!', 'error')
        return redirect(url_for('login'))

    if session.get('role') == 'admin':
        flash('Admin không thể thao tác giỏ hàng!', 'error')
        return redirect(url_for('index'))

    cart = session.get('cart', {})
    key = str(product_id)

    if key in cart:
        del cart[key]
        session['cart'] = cart
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'success')
    else:
        flash('Sản phẩm không tồn tại trong giỏ hàng!', 'info')

    return redirect(url_for('view_cart'))








@app.route('/buy_now/<int:product_id>')
def buy_now(product_id):
    # Thêm vào giỏ trước
    add_to_cart(product_id, quantity=1)
    return redirect(url_for('view_cart'))  # Đi thẳng đến trang giỏ để đặt hàng


@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash('Đã xóa giỏ hàng!', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập để xem hồ sơ!', 'error')
        return redirect(url_for('login'))
    conn = get_db_connection()
    try:
        user = conn.execute("""
            SELECT 
                id,
                username,
                email,
                phone,
                dob,
                address,
                role,
                avatar
            FROM users 
            WHERE id = ?
        """, (session['user_id'],)).fetchone()

        if user is None:
            flash('Không tìm thấy thông tin người dùng.', 'error')
            conn.close()
            return redirect(url_for('logout'))

        # Chuyển sqlite3.Row thành dict để dễ dùng trong template hơn (tùy chọn)
        user_dict = dict(user)

    except Exception as e:
        flash('Lỗi tải thông tin hồ sơ.', 'error')
        conn.close()
        return redirect(url_for('index'))
    finally:
        conn.close()
    return render_template('profile.html', user=user_dict)
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập!', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        phone = request.form.get('phone').strip()
        dob = request.form.get('dob')
        address = request.form.get('address').strip()
        avatar_file = request.files.get('avatar')

        # Handle avatar upload
        avatar_filename = None
        old_avatar = conn.execute('SELECT avatar FROM users WHERE id = ?', 
                                  (session['user_id'],)).fetchone()['avatar']

        if avatar_file and allowed_file(avatar_file.filename):
            safe_name = secure_filename(avatar_file.filename)
            avatar_filename = f"{session['username']}_{uuid.uuid4().hex}_{safe_name}"
            avatar_file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))

            # Delete old avatar if exists and is not the default/placeholder
            if old_avatar:
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_avatar)
                if os.path.exists(old_path):
                    os.remove(old_path)
        else:
            avatar_filename = old_avatar  # keep old avatar if no new file

        # Update user info
        try:
            conn.execute("""
                UPDATE users 
                SET phone = ?, dob = ?, address = ?, avatar = ?
                WHERE id = ?
            """, (phone, dob, address, avatar_filename, session['user_id']))
            conn.commit()
            flash('Cập nhật hồ sơ thành công!', 'success')

            # Update session username if needed (in case you want to use it elsewhere)
            # session['username'] remains the same because username cannot be changed here

            return redirect(url_for('profile'))

        except Exception as e:
            flash('Có lỗi xảy ra khi cập nhật hồ sơ.', 'error')
            print(e)
        finally:
            conn.close()

    # GET request → show edit form
    user = conn.execute("""
        SELECT username, email, phone, dob, address, avatar, role
        FROM users WHERE id = ?
    """, (session['user_id'],)).fetchone()
    conn.close()

    if user is None:
        flash('Không tìm thấy người dùng.', 'error')
        return redirect(url_for('logout'))

    return render_template('edit_profile.html', user=user)










# Routes category
# Các route này PHẢI render template, không được return string.
# Template đang gọi url_for('dienthoai'), url_for('laptop')... nên endpoint phải tồn tại
# và phải hiển thị trang sản phẩm theo danh mục.
CATEGORY_ENDPOINTS = {
    'dienthoai': 'dienthoai',
    'tulanh':    'tulanh',
    'dongho':    'dongho',
    'laptop':    'laptop',
    'mayanh':    'mayanh',
    'dieuhoa':   'dieuhoa',
    'tainghe':   'tainghe',
}
VALID_CATEGORIES = {
    'dienthoai': 'Điện Thoại',
    'dongho': 'Đồng Hồ Thông Minh',
    'laptop': 'Laptop',
    'maytinhbanpc': 'Máy Tính Bàn / PC',
    'tulanh': 'Tủ Lạnh',
    'quat': 'Quạt',
    'maygiatsay': 'Máy Giặt & Sấy',
    'beptu': 'Bếp Từ'
}


def _render_category(category):
    """Render trang danh mục dùng chung cho mọi alias route bên dưới."""
    page = request.args.get('page', 1, type=int)
    per_page = 12

    conn = get_db_connection()
    total = conn.execute(
        "SELECT COUNT(*) FROM products WHERE category = ?",
        (category,)
    ).fetchone()[0]

    products = conn.execute("""
        SELECT id, product_id, name, category, brand, price, image,
               cpu, display, ram, storage, gpu, battery, camera,
               chip, sensor, water_resistance,
               ports, wifi, cooling,
               capacity, type, cooling_tech, energy_rating, motor, technology, warranty, shelves,
               power, speed_levels, control_type, oscillation, timer, size, blade_type, filter,
               zones, burners, grates, safety, ignition
        FROM products
        WHERE category = ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (category, per_page, (page - 1) * per_page)).fetchall()
    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template('category.html',
                           products=products,
                           category_name=VALID_CATEGORIES.get(category, category),
                           category_key=category,
                           page=page,
                           total_pages=total_pages,
                           total_products=total)


@app.route('/dienthoai')
def dienthoai():
    return _render_category('dienthoai')

@app.route('/tulanh')
def tulanh():
    return _render_category('tulanh')

@app.route('/dongho')
def dongho():
    return _render_category('dongho')

@app.route('/laptop')
def laptop():
    return _render_category('laptop')

@app.route('/mayanh')
def mayanh():
    return _render_category('mayanh')

@app.route('/dieuhoa')
def dieuhoa():
    return _render_category('dieuhoa')

@app.route('/tainghe')
def tainghe():
    return _render_category('tainghe')

@app.route('/maytinh')
def man_hinh_may_tinh():
    return _render_category('maytinhbanpc')


@app.route('/category/<category>')
def category_products(category):
    """Hiển thị sản phẩm theo danh mục"""
    # Danh sách danh mục hợp lệ (dùng chung hằng số VALID_CATEGORIES)
    valid_categories = VALID_CATEGORIES

    if category not in valid_categories:
        flash('Danh mục không tồn tại!', 'danger')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    per_page = 12  # Số sản phẩm mỗi trang

    conn = get_db_connection()

    # Đếm tổng sản phẩm trong danh mục
    total = conn.execute(
        "SELECT COUNT(*) FROM products WHERE category = ?",
        (category,)
    ).fetchone()[0]

    # Lấy sản phẩm cho trang hiện tại + tất cả specs để hiển thị
    products = conn.execute("""
        SELECT id, product_id, name, category, brand, price, image,
               cpu, display, ram, storage, gpu, battery, camera,
               chip, sensor, water_resistance,
               ports, wifi, cooling,
               capacity, type, cooling_tech, energy_rating, motor, technology, warranty, shelves,
               power, speed_levels, control_type, oscillation, timer, size, blade_type, filter,
               zones, burners, grates, safety, ignition
        FROM products
        WHERE category = ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (category, per_page, (page - 1) * per_page)).fetchall()

    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template('category.html',
                           products=products,
                           category_name=valid_categories[category],
                           category_key=category,
                           page=page,
                           total_pages=total_pages,
                           total_products=total)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()

    if not query:
        flash('Vui lòng nhập từ khóa tìm kiếm!', 'warning')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    per_page = 12

    conn = get_db_connection()

    # Tìm kiếm trong tên sản phẩm, thương hiệu, và các thông số phổ biến
    search_pattern = f"%{query}%"
    products = conn.execute("""
        SELECT id, product_id, name, category, brand, price, image,
               cpu, display, ram, storage, gpu, battery, camera,
               chip, sensor, water_resistance,
               ports, wifi, cooling,
               capacity, type, cooling_tech, energy_rating, motor, technology, warranty, shelves,
               power, speed_levels, control_type, oscillation, timer, size, blade_type, filter,
               zones, burners, grates, safety, ignition
        FROM products
        WHERE name LIKE ?
           OR brand LIKE ?
           OR cpu LIKE ?
           OR display LIKE ?
           OR ram LIKE ?
           OR storage LIKE ?
           OR camera LIKE ?
           OR capacity LIKE ?
        ORDER BY
            CASE
                WHEN name LIKE ? THEN 1
                WHEN brand LIKE ? THEN 2
                ELSE 3
            END,
            name
        LIMIT ? OFFSET ?
    """, (search_pattern, search_pattern, search_pattern, search_pattern,
          search_pattern, search_pattern, search_pattern, search_pattern,
          search_pattern, search_pattern,
          per_page, (page - 1) * per_page)).fetchall()

    # Đếm tổng kết quả
    total = conn.execute("""
        SELECT COUNT(*) FROM products
        WHERE name LIKE ?
           OR brand LIKE ?
           OR cpu LIKE ?
           OR display LIKE ?
           OR ram LIKE ?
           OR storage LIKE ?
           OR camera LIKE ?
           OR capacity LIKE ?
    """, (search_pattern, search_pattern, search_pattern, search_pattern,
          search_pattern, search_pattern, search_pattern, search_pattern)).fetchone()[0]

    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template('search_results.html',
                           products=products,
                           query=query,
                           total_products=total,
                           page=page,
                           total_pages=total_pages)


@app.route('/lienhe', methods=['GET', 'POST'])
def lienhe():
    """Trang liên hệ - chỉ định nghĩa MỘT lần duy nhất."""
    if request.method == 'POST':
        flash('Cảm ơn bạn đã gửi liên hệ!', 'success')
        return redirect(url_for('lienhe'))
    return render_template('lienhe.html')


# === RUN APP ===
if __name__ == '__main__':
    app.run(debug=True)








