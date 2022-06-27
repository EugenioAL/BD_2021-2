from psycopg2 import connect

def get_connection():
    return connect("dbname=postgres user=postgres password=postgres host=0.0.0.0 port=5432")

def letra_a():
    print("asin: 0486220125")

    sql = f"""
            select utils.*
            from (
                (
                    select revs.*
                    from (
                        select * 
                        from reviews 
                        where ( 
                            votes > 0 and ((helpfull* 100)/votes > 50) and rating > 2) 
                        ) revs
                    where revs.asin_product = '0486220125'
                    order by revs.rating desc, revs.helpfull desc
                    limit 5
                )
                union all
                (
                    select revs.*
                    from (
                        select * 
                        from reviews 
                        where ( 
                            votes > 0 and ((helpfull*100)/votes > 50) and rating > 2) 
                        ) revs
                    where revs.asin_product = '0486220125'
                    order by revs.rating, revs.helpfull desc
                    limit 5
                )
            ) utils;
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        print(result)
    cur.close()
    conn.close()

def letra_b():
    print("asin: 0380788101")

    sql = f"""
            select *
            from products as prod
            where prod.asin in (
                select asin_product_2
                from similars
                where similars.asin_product_1 = '0380788101'
            )
            and prod.salesrank < (select salesrank from products where asin = '0380788101');
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        print(result)
    cur.close()
    conn.close()

def letra_d():

    sql = f"""
            select prod.ranking, prod.product_group, prod.asin, prod.salesrank, prod.title
            from 
                (
                    select
                    row_number() over (partition by product_group order by salesrank asc) as ranking,
                    t.*
                    from products t
                ) prod
            where prod.ranking <= 10 and prod.salesrank > 0;
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        print(result)
    cur.close()
    conn.close()

def letra_e():
    sql = f"""
            select prod.asin, products.title, prod.avrrating, prod.total_reviews 
            from (
                select revs.asin_product as asin, avg(revs.rating) as avrrating, count(revs.rating) as total_reviews
                from (
                    select * 
                    from reviews 
                    where ( votes > 0 and ((helpfull*100)/votes) > 50 and rating > 2) 
                    ) revs
                group by asin_product
                ) prod, products
            where products.asin = prod.asin
            order by prod.avrrating desc, prod.total_reviews desc
            limit 10
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        print(result)
    cur.close()
    conn.close()

def letra_f():
    sql = f"""
            select categories.id, categories.title 
            from categories,(
                select prod.category_id, sum(prod.avrrating) as most_avg_rating 
                from (
                    select * 
                    from (
                        select asin_product, avg(rating) as avrrating, count(asin_product) as total_reviews 
                        from (
                            select * 
                            from reviews 
                            where ( votes > 0 and ((helpfull*100)/votes) > 50 and rating > 2) 
                        ) revs
                        group by asin_product
                    ) product_rating,
                    (
                        select products.asin, categories.title as category_name, categories.id as category_id 
                        from products, categories, product_categories 
                        where (
                            product_categories.id_category = categories.id and product_categories.asin_product = products.asin
                        )
                    ) product_categories
                    where product_rating.asin_product = product_categories.asin
                    order by avrrating desc,total_reviews desc
                ) prod
                group by prod.category_id
            ) category_rating
            where categories.id = category_rating.category_id
            order by category_rating.most_avg_rating desc
            limit 5
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)

    results = cur.fetchall()
    for result in results:
        print(result)
    cur.close()
    conn.close()

def letra_g():
    sql = f"""
            select * 
            from (
                select
                row_number() over (partition by product_group order by number_coments desc) AS ranking,
                all_comm_by_group.*
                from (
                    select prod.product_group, prod.customer, prod.number_coments
                    from (
                        select products.product_group, reviews.customer, count(reviews.customer) as number_coments
                        from products, reviews 
                        where products.asin = reviews.asin_product 
                        group by (products.product_group, reviews.customer)
                    ) prod
                ) all_comm_by_group
            ) limit_comm_by_group
            where limit_comm_by_group.ranking <= 10;
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        print(result)

    cur.close()
    conn.close()
    

def main():
    print("** consultas **")
    letra_a()
    letra_b()
    letra_d()
    letra_e()
    letra_f()
    letra_g()

    
if __name__ == "__main__":
    main()
