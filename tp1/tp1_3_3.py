from psycopg2 import connect

def get_connection():
    return connect("dbname=postgres user=postgres password=postgres host=0.0.0.0 port=5432")

def letra_a():
    print("asin: 0486220125")

    sql = f"""
        select maisUteis.customer, maisUteis.rating, maisUteis.helpful, maisUteis.votes
        from (
            select *
            from produto p
            join review r ON r.asin = p.asin
            where p.asin = '0738700797'
            order by r.helpful desc
            limit 10
            ) as maisUteis
        order by maisUteis.rating desc;
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
    x = '0380788101'

    sql = f"""
            select *
            from produto as prod
            where prod.asin in (
                select asin_sim
                from similares
                where similares.asin = '0380788101'
            )
            and prod.salesrank < (select salesrank from produto where asin = '0380788101');
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
            select prod.ranking, prod.grupo, prod.asin, prod.salesrank, prod.title
            from
                (
                    select
                    row_number() over (partition by grupo order by salesrank asc) as ranking,
                    p.*
                    from produto p
                    where p.salesrank > 0
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
            select prod.asin, produto.title, prod.avrrating, prod.total_votes
            from (
                select revs.asin as asin, avg(revs.rating) as avrrating, count(revs.votes) as total_votes
                from (
                    select *
                    from review r
                    where ( r.votes > 0 )
                    ) revs
                group by revs.asin
                ) prod, produto
            where produto.asin = prod.asin
            order by prod.avrrating desc, prod.total_votes desc
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
            select categoria.id, categoria.nome
            from categoria,(
                select prod.category_id, avg(prod.avrrating) as most_avg_rating, sum(prod.total_votes) as most_votes
                from (
                    select *
                    from (
                        select asin, avg(rating) as avrrating, count(votes) as total_votes
                        from (
                            select *
                            from review r
                            where ( r.votes > 0)
                        ) revs
                        group by revs.asin
                    ) product_rating,
                    (
                        select produto.asin, categoria.nome as category_name, categoria.id as category_id
                        from produto, categoria, produtocategoria p
                        where (
                            p.id_categoria = categoria.id and p.asin = produto.asin
                        )
                    ) product_categories
                    where product_rating.asin = product_categories.asin
                    order by avrrating desc,total_votes desc
                ) prod
                group by prod.category_id
            ) category_rating
            where categoria.id = category_rating.category_id
            order by category_rating.most_avg_rating desc, category_rating.most_votes desc
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
                row_number() over (partition by grupo order by number_comments desc) AS ranking,
                all_comm_by_group.*
                from (
                    select prod.grupo, prod.customer, prod.number_comments
                    from (
                        select produto.grupo, review.customer, count(review.customer) as number_comments
                        from produto, review
                        where produto.asin = review.asin
                        group by (produto.grupo, review.customer)
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
