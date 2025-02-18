import sqlite3
from flask import Flask, g , render_template, request, redirect, url_for 

DATABASE = 'database.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    """データベースに接続"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row # 結果を辞書形式で取得
    return rv

def get_db():
    """データベース接続を取得、リクエストごとにコネクションを再利用"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """リクエスト終了時にデータベース接続を閉じる"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    """データベースを初期化"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

if __name__ == '__main__':
    #データベースの初期化処理
    with app.app_context():
        init_db()

@app.route('/')
def index():
    """書籍一覧を表示する"""
    db = get_db()
    cur = db.execute('SELECT * FROM books')
    books = cur.fetchall()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    """書籍を追加"""
    title = request.form['title']
    author = request.form['author']
    publisher = request.form['publisher']
    publication_date = request.form['publication_date']
    genre = request.form['genre']
    status = request.form['status']
    rating = request.form['rating']
    memo = request.form['memo']

    db = get_db()
    db.execute('INSERT INTO books (title, author, publisher, publication_date, genre, status, rating, memo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [title, author, publisher, publication_date, genre, status, rating, memo])
    db.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:book_id>')
def edit_book(book_id):
    """書籍編集ページを表示"""
    db = get_db()
    cur = db.execute('SELECT * FROM books WHERE id = ?', [book_id])
    book = cur.fetchall()
    if not book:
        return redirect(url_for('index'))  # 書籍が見つからない場合はリダイレクト
    return render_template('edit.html', book=book)

@app.route('/update/<int:book_id>', methods=['POST'])
def update_book(book_id):
    """書籍情報を更新"""
    title = request.form['title']
    author = request.form['author']
    publisher = request.form['publisher']
    publication_date = request.form['publication_date']
    genre = request.form['genre']
    status = request.form['status']
    rating = request.form['rating']
    memo = request.form['memo']
    
    db = get_db()
    db.execute('UPDATE books SET title = ?, author = ?, publisher = ?, publication_date = ?, genre = ?, status = ?, rating = ?, memo = ? WHERE id = ?', [title, author, publisher, publication_date, genre, status, rating, memo, book_id])
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    """書籍の削除"""
    db = get_db()
    db.execute('DELETE FROM books WHERE id = ?', [book_id])
    db.commit()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)