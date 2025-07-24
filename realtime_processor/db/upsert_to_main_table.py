import psycopg2


def upsert_to_main_table():
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
            INSERT INTO pharmaceutical_data AS main
            SELECT * FROM pharmaceutical_data_staging
            ON CONFLICT (soDangKy)
            DO UPDATE SET
                idThuoc = EXCLUDED.idThuoc,
                phanLoaiThuocEnum = EXCLUDED.phanLoaiThuocEnum,
                tenCongTyDangKy = EXCLUDED.tenCongTyDangKy,
                diaChiDangKy = EXCLUDED.diaChiDangKy,
                nuocDangKy = EXCLUDED.nuocDangKy,
                congTyDangKyId = EXCLUDED.congTyDangKyId,
                tenCongTySanXuat = EXCLUDED.tenCongTySanXuat,
                diaChiSanXuat = EXCLUDED.diaChiSanXuat,
                nuocSanXuat = EXCLUDED.nuocSanXuat,
                congTySanXuatId = EXCLUDED.congTySanXuatId,
                fullAddress = EXCLUDED.fullAddress,
                soDangKyCu = EXCLUDED.soDangKyCu,
                tenThuoc = EXCLUDED.tenThuoc,
                dotCap = EXCLUDED.dotCap,
                ngayCapSoDangKy = EXCLUDED.ngayCapSoDangKy,
                ngayHetHanSoDangKy = EXCLUDED.ngayHetHanSoDangKy,
                ngayGiaHanSoDangKy = EXCLUDED.ngayGiaHanSoDangKy,
                soQuyetDinh = EXCLUDED.soQuyetDinh,
                thongTinRutSoDangKy = EXCLUDED.thongTinRutSoDangKy,
                dangBaoChe = EXCLUDED.dangBaoChe,
                dongGoi = EXCLUDED.dongGoi,
                hamLuong = EXCLUDED.hamLuong,
                hoatChatChinh = EXCLUDED.hoatChatChinh,
                tieuChuan = EXCLUDED.tieuChuan,
                tieuChuanId = EXCLUDED.tieuChuanId,
                tuoiTho = EXCLUDED.tuoiTho,
                creationTime = EXCLUDED.creationTime,
                lastModificationTime = EXCLUDED.lastModificationTime

            """)

        print("Table upsert successfully in PostgreSQL")
        cursor.execute("TRUNCATE TABLE pharmaceutical_data_staging;")
        print("Truncated staging table successfully")

        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()