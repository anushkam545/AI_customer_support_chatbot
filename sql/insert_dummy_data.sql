-- ============================================================
-- Bookleaf Publishing — Dummy Data
-- ============================================================


-- ------------------------------------------------------------
-- Customers
-- ------------------------------------------------------------
INSERT INTO customers (customer_id, customer_name, email, phone, country, created_at) VALUES
    ('CUST001', 'James Whitmore',  'james.whitmore@email.com',  '+1-312-555-0184', 'United States', '2024-01-15 09:22:00'),
    ('CUST002', 'Sarah O''Brien',  'sarah.obrien@email.com',    '+44-20-7946-0321', 'United Kingdom', '2024-02-03 11:45:00'),
    ('CUST003', 'Priya Sharma',    'priya.sharma@email.com',    '+91-98201-56234', 'India',          '2024-03-18 14:10:00'),
    ('CUST004', 'Marcus Chen',     'marcus.chen@email.com',     '+1-604-555-0273', 'Canada',         '2024-04-07 08:55:00'),
    ('CUST005', 'Emma Klaas',      'emma.klaas@email.com',      '+61-2-5550-3892', 'Australia',      '2024-05-22 16:30:00');


-- ------------------------------------------------------------
-- Books
-- ------------------------------------------------------------
INSERT INTO books (
    book_id, customer_id, book_title,
    final_submission_date, book_live_date,
    royalty_status, isbn, add_on_services,
    manuscript_status, current_stage
) VALUES
    (
        'BOOK001', 'CUST001',
        'The Resilient Entrepreneur: Building Businesses That Last',
        '2024-03-01', '2024-06-15',
        'Paid', '978-1-7392841-0-1',
        'Professional Editing, Cover Design, Marketing Package',
        'Final Approved', 'Live'
    ),
    (
        'BOOK002', 'CUST002',
        'Threads of Time: A Memoir of Family, Loss and Hope',
        '2024-04-20', '2024-08-10',
        'Processing', '978-1-7392841-1-8',
        'Proofreading, Cover Design, Audiobook Conversion',
        'Approved', 'Pre-Publishing Review'
    ),
    (
        'BOOK003', 'CUST003',
        'Mindful Every Day: Simple Practices for a Balanced Life',
        '2024-05-30', NULL,
        'Pending', NULL,
        'Professional Editing, Proofreading, Interior Formatting',
        'Revision Requested', 'Editing'
    ),
    (
        'BOOK004', 'CUST004',
        'Echoes of the Forgotten City',
        '2024-06-15', NULL,
        'Pending', NULL,
        'Cover Design, Interior Formatting',
        'Under Review', 'Manuscript Received'
    ),
    (
        'BOOK005', 'CUST005',
        'Pip and the Rainbow Garden',
        '2024-04-10', '2024-07-01',
        'Paid', '978-1-7392841-2-5',
        'Illustration Review, Cover Design, Marketing Package',
        'Final Approved', 'Live'
    );


-- ------------------------------------------------------------
-- Support Tickets
-- ------------------------------------------------------------
INSERT INTO support_tickets (ticket_id, customer_id, issue, status, created_at) VALUES
    (
        'TKT001', 'CUST001',
        'Royalty payment for BOOK001 was marked as Paid but funds have not arrived in my bank account after 10 business days.',
        'Resolved',
        '2024-07-02 10:15:00'
    ),
    (
        'TKT002', 'CUST002',
        'My book BOOK002 has been in Pre-Publishing Review for over three weeks. Requesting an update on the expected live date.',
        'In Progress',
        '2024-08-01 13:40:00'
    ),
    (
        'TKT003', 'CUST003',
        'Received a revision request for BOOK003 but the feedback document attached to the email appears to be corrupted and cannot be opened.',
        'Open',
        '2024-08-05 09:05:00'
    ),
    (
        'TKT004', 'CUST004',
        'Uploaded the manuscript for BOOK004 four days ago but the portal still shows no confirmation of receipt.',
        'Open',
        '2024-08-06 15:22:00'
    ),
    (
        'TKT005', 'CUST005',
        'BOOK005 is live but the author bio on the product page contains a spelling error. Please update "Australi" to "Australia".',
        'Closed',
        '2024-07-08 11:00:00'
    );


-- ------------------------------------------------------------
-- Documents (Knowledge Base — embeddings populated at runtime)
-- ------------------------------------------------------------
INSERT INTO documents (title, content) VALUES
    (
        'Royalty Payment Schedule',
        'Bookleaf Publishing processes royalty payments on a quarterly basis. Payment periods close on the last day of March, June, September, and December. Funds are transferred within 10 to 15 business days after the period closes. Authors must ensure their bank or PayPal details are up to date in the Author Portal before the period closes to avoid delays. If a payment is overdue beyond 15 business days, authors should raise a support ticket referencing their Book ID.'
    ),
    (
        'Manuscript Submission Guidelines',
        'Authors must submit manuscripts in .docx or .pdf format via the Bookleaf Author Portal. The maximum file size is 50 MB. Manuscripts should use 12pt Times New Roman, double line spacing, and 2.5 cm margins on all sides. All images must be embedded at 300 DPI. Once submitted, authors receive an automated confirmation email within 24 hours. If no confirmation is received, authors should check their spam folder or contact support with their Customer ID.'
    ),
    (
        'Publishing Stages Explained',
        'After manuscript submission, a book moves through the following stages: Manuscript Received, Editing, Proofreading, Cover Design, ISBN Assignment, Pre-Publishing Review, and finally Live. Each stage requires author approval before progressing. Average total time from submission to Live is 10 to 14 weeks depending on the add-on services selected. Authors can track their current stage at any time through the Author Portal dashboard.'
    ),
    (
        'Add-On Services Overview',
        'Bookleaf Publishing offers the following add-on services: Professional Editing (developmental and line editing by a qualified editor), Proofreading (final grammar and consistency check), Cover Design (custom design with two revision rounds), Interior Formatting (typesetting for print and eBook), Audiobook Conversion (narration and mastering), Illustration Review (for children''s and illustrated books), and Marketing Package (press release, social media kit, and Amazon optimisation). Services must be selected and paid for before the manuscript enters the editing stage.'
    ),
    (
        'ISBN and Copyright Information',
        'Bookleaf Publishing assigns a free ISBN to every published book. The ISBN is registered under the Bookleaf Publishing imprint unless the author requests a custom imprint at an additional fee. Authors retain full copyright of their work at all times. The ISBN is issued during the ISBN Assignment stage and will appear on the book cover, copyright page, and all retail listings. Authors who already own an ISBN may provide it during manuscript submission.'
    );
