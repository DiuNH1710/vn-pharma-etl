import psycopg2

def create_table():
    conn = None
    try:
        # connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="123456",
            host="host.docker.internal",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pharmaceutical_data (
            idThuoc INTEGER, 
            phanLoaiThuocEnum INTEGER,
            tenCongTyDangKy TEXT,
            diaChiDangKy TEXT,
            nuocDangKy TEXT,
            congTyDangKyId INTEGER,
            tenCongTySanXuat TEXT,
            diaChiSanXuat TEXT,
            nuocSanXuat TEXT,
            congTySanXuatId INTEGER, 
            fullAddress TEXT,
            soDangKy TEXT PRIMARY KEY,
            soDangKyCu TEXT,
            tenThuoc TEXT,
            dotCap TEXT,
            ngayCapSoDangKy TIMESTAMP,
            ngayHetHanSoDangKy TIMESTAMP,
            ngayGiaHanSoDangKy TIMESTAMP,
            soQuyetDinh TEXT,
            thongTinRutSoDangKy TEXT,
            dangBaoChe TEXT,
            dongGoi TEXT,
            hamLuong TEXT,
            hoatChatChinh TEXT,
            tieuChuan TEXT,
            tieuChuanId TEXT,
            tuoiTho TEXT,
            creationTime TIMESTAMP,
            lastModificationTime TIMESTAMP

        );
        """)

        print("Table main created successfully in PostgreSQL")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pharmaceutical_data_staging (
            LIKE pharmaceutical_data INCLUDING DEFAULTS EXCLUDING CONSTRAINTS
            );
        """)

        print("Table staging created successfully in PostgreSQL")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()