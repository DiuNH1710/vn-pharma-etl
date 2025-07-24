import psycopg2


def create_table():
    conn = None
    try:
        # connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="123456",
            host="localhost",
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
            soDangKy TEXT ,
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
            lastModificationTime TIMESTAMP,
            crawlTime TIMESTAMP

        );
        """)
        conn.commit()

        print("Table created successfully in PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()