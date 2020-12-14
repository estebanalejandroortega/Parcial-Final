from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
app = Flask(__name__)
app.secret_key = 'n4P1wkCa2kwFZmXa4Rya6NK9CowfSDw6JTo9OhIxmjwhUywUyf'
db = sqlite3.connect('data.db', check_same_thread=False)

@app.route('/', methods =['GET', 'POST'])
def inicio():
    if request.method == 'GET':
        return render_template('inicio.html')
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena')
    cursor = db.cursor()
    if correo == '' or contrasena == '':
        flash('Todos los campos son obligatorios')
        return redirect(request.url)
    usuario = cursor.execute(""" SELECT * FROM usuarios WHERE correo = ? and contrasena = ?""",(correo,contrasena,)).fetchone()
    if usuario is None:
        flash('Correo y Contraseña Inválidos')
        return redirect(request.url)
    session['usuario'] = usuario
    return redirect(url_for('categorias'))

@app.route('/usuario/crear', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'GET':
        return render_template('crear_usuario.html')
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena')
    if nombre == '' or correo == '' or contrasena == '':
        flash('Todos los campos son obligatorios')
        return redirect(request.url)
    try:
        cursor = db.cursor()
        cursor.execute(""" INSERT INTO usuarios (nombre,correo,contrasena) VALUES (?,?,?) """,(nombre,correo,contrasena,))
        db.commit()
    except:
        flash('No se ha podido guardar el registro de usuario')
        return redirect(request.url)
    flash('El usuario ha sido registrado correctamente')
    return redirect(url_for('categorias'))

@app.route('/categorias')
def categorias():
    if not 'usuario' in session:
        return redirect(url_for('inicio'))
    categorias = db.execute("""SELECT * FROM categorias WHERE id_usuario = ?""",(session['usuario'][0],)).fetchall()
    return render_template('categorias.html', categorias = categorias)

@app.route('/productos')
def productos():
    if not 'usuario' in session:
        return redirect(url_for('inicio'))
    productos = db.execute("""SELECT * FROM productos WHERE id_usuario = ?""",(session['usuario'][0],)).fetchall()
    return render_template('productos.html', productos = productos )

@app.route('/usuario', methods=['GET','POST'])
def usuario():
    if not 'usuario' in session:
        return redirect(url_for('inicio'))
    if request.method == 'GET':
        usuario = db.execute(""" SELECT * FROM  usuarios WHERE id_usuario = ?""",(session['usuario'][0],)).fetchone()
        return render_template('usuario.html', usuario = usuario)
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena')
    if nombre == '' or correo == '' or contrasena == '':
        flash('Todos los campos son obligatorios')
        return redirect(request.url)
    try:
        cursor = db.cursor()
        cursor.execute(""" UPDATE usuarios SET nombre = ?,correo = ?,contrasena = ? WHERE id_usuario = ? """,(nombre,correo,contrasena,session['usuario'][0],))
        db.commit()
    except:
        flash('Este correo ya se encuentra en uso')
        return redirect(request.url)
    flash('Usuario actualizado correctamente')
    return redirect(url_for('usuario'))

@app.route('/categorias/crear', methods=['GET','POST'])
def crear_categoria():
    if not 'usuario' in session:
        return redirect(url_for('inicio'))
    if request.method == 'GET':
        return render_template('crear_categorias.html')
    categoria = request.form.get('categoria')
    if categoria == '':
        flash('Todos los campos son obligatorios')
        return redirect(request.url)
    try:
        cursor = db.cursor()
        cursor.execute("""INSERT INTO categorias(id_usuario, nombre_categoria) VALUES (?,?)""",(session['usuario'][0],categoria,))
        db.commit()
    except:
        flash('Categoria ya se encuentra creada')
        return(redirect(request.url))
    flash('Categoria creada correctamente')
    return redirect(url_for('categorias'))

@app.route('/productos/crear', methods = ['GET','POST'])
def crear_producto():
    if not 'usuario' in session:
        return redirect(url_for('inicio'))
    if request.method == 'GET':
        categorias = db.execute("""SELECT * FROM categorias WHERE id_usuario = ?""",(session['usuario'][0],)).fetchall()
        return render_template('crear_producto.html', categorias = categorias)
    producto = request.form.get('producto')
    precio = request.form.get('precio')
    categoria = request.form.get('categoria')
    if producto == '' or precio == '' or categoria == '':
        flash('Todos los campos son obligatorios')
        return redirect(request.url)
    try:
        cursor = db.cursor()
        cursor.execute("""INSERT INTO productos(id_usuario,nombre_categoria,nombre_producto,precio) VALUES (?,?,?,?)""",(session['usuario'][0],categoria,producto,precio,))
        db.commit()
    except:
        flash('Producto ya se encuentra creado')
        return redirect(request.url)
    flash('Producto creado correctamente')
    return redirect(url_for('productos'))

@app.route('/categorias/editar/<int:id>', methods=['GET','POST'])
def editar_categoria(id):
    if not 'usuario' in session:
        return redirect(url_for('inicio'))
    if request.method == 'GET':  
        categoria = db.execute(""" SELECT * FROM categorias WHERE id_categoria = ? """,(id,)).fetchone()
        return render_template('editar_categoria.html', categoria = categoria)
    nombre = request.form.get('categoria')
    if nombre == '':
        flash('Todos los campos son obligatorios')
        return redirect(request.url)
    try:
        cursor = db.cursor()
        cursor.execute(""" UPDATE categorias SET nombre_categoria = ? WHERE id_categoria = ?""",(nombre,id,))
        db.commit()
    except:
        flash('Categoria ya se encuentra creada ')
        return(redirect(request.url))
    flash('Categoria editada correctamente')
    return redirect(url_for('categorias'))

@app.route('/productos/editar/<int:id>', methods=['GET','POST'])
def editar_producto(id):
    if not 'usuario' in session:
        return redirect(url_for('inicio'))
    if request.method == 'GET':
        categorias = db.execute("""SELECT * FROM categorias WHERE id_usuario = ?""",(session['usuario'][0],)).fetchall()
        producto = db.execute("""SELECT * FROM productos WHERE id_producto = ?""",(id,)).fetchone()
        return render_template('editar_producto.html', producto = producto, categorias = categorias)
    producto = request.form.get('producto')
    precio = request.form.get('precio')
    categoria = request.form.get('categoria')
    if producto == '' or precio == '' or categoria == '':
        flash('Todos los campos son obligatorios')
        return redirect(request.url)
    try:
        cursor = db.cursor()
        cursor.execute(""" UPDATE productos SET nombre_producto = ?, precio = ?, nombre_categoria = ? WHERE id_producto = ? """,(producto,precio,categoria,id))
        db.commit()
    except:
        flash('Producto ya se encuentra creado')
        return redirect(request.url)
    flash('Producto actualizado correctamente')
    return redirect(url_for('productos'))

@app.route('/categorias/eliminar/<int:id>')
def eliminar_categoria(id):
    if not 'usuario' in session:
        return redirect(url_for('inicio'))
    cursor = db.cursor()
    flash('Categoria eliminada correctamente')
    cursor.execute(""" DELETE FROM categorias WHERE id_categoria = ?""",(id,))
    db.commit()
    return redirect(url_for('categorias'))

@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    if not 'usuario' in session:
        return redirect(url_for('inicio'))
    db.execute(""" DELETE FROM productos WHERE id_producto = ? """,(id,))
    db.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('productos'))

@app.route('/salir')
def cerrar_sesion():
    session.clear()
    return redirect(url_for('inicio'))
app.run(debug=True)